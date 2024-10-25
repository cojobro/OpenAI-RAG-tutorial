import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = os.environ.get("PINECONE_INDEX")  

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

retriever = vector_store.as_retriever()

llm = ChatOpenAI(model="gpt-4o-mini")

temp_prompt = (
    "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If the answer is not provided in the context, tell the user that you do not have the context required to know the answer.\n\n"
    "Context: {context}\n\n"
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", temp_prompt),
        ("human", "{input}"),
    ]
)
#if you want to bring the list out of the prompt to update conversational memory, "system" is role of the model, "human" is user input, and "ai" is response of model

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

query = "What did the gladiators do?"

response = rag_chain.invoke({"input":query})
print(response["answer"])