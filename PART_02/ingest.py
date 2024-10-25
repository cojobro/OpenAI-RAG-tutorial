import os
import re
import time
import glob
from dotenv import load_dotenv
from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm

load_dotenv()

client = OpenAI()

MODEL = "text-embedding-3-small"

res = client.embeddings.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
        ], 
    model=MODEL
)

# we can extract embeddings to a list
embeds = [record.embedding for record in res.data]
len(embeds)

# Initialize Pinecone
pc = Pinecone()

spec = ServerlessSpec(cloud=os.environ.get("PINECONE_CLOUD"), region=os.environ.get("PINECONE_REGION"))

# Define the index name
index_name = os.environ.get("PINECONE_INDEX")

# Create the index if it doesn't exist
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=len(embeds[0]),  # dimensionality of text-embed-3-small
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# Instantiate the index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()

# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

metadata = []

def process_pdf(file_path):
    # create a loader
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc.page_content) for doc in documents]
    metadata.extend(doc.metadata for doc in documents)
    return texts

# Initialize an empty list to hold all texts
texts = []

# Process all PDF files in the 'docs' folder
for file_path in glob.glob('./docs/*.pdf'):
    texts.extend(process_pdf(file_path))

print(len(metadata))
print(len(texts))
count = 0  # we'll use the count to create unique IDs
batch_size = 32  # process everything in batches of 32

for i in tqdm(range(0, len(texts), batch_size)):
    # set end position of batch
    i_end = min(i+batch_size, len(texts))
    # get batch of lines and IDs
    lines_batch = texts[i: i_end]
    meta_batch = metadata[i: i_end]
    ids_batch = [str(n) for n in range(i, i_end)]
    # create embeddings
    res = client.embeddings.create(input=lines_batch, model=MODEL)
    embeds = [record.embedding for record in res.data]
    # prep metadata and upsert batch
    meta = [{'text': line, 'source': meta['source'], 'page': meta['page']} for line, meta in zip(lines_batch, meta_batch)]
    to_upsert = zip(ids_batch, embeds, meta)
    # upsert to Pinecone
    index.upsert(vectors=list(to_upsert))