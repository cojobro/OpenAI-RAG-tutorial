# OpenAI-RAG-tutorial
Hello and welcome! This is a three-stage tutorial to educate how to effectively implement Retrieval Augmented Generation (RAG) using OpenAI, Pinecone, and Langchain.

The three parts of this tutorial include:

1) Building an AI Chatbot
2) Embedding PDFs into a vector space
3) Building a simple RAG application

Each of the folders labeled parts 1-3 each have a respective tutorial video to follow along.



I strongly recommend using a virtual environment to create an isolated and stable version of Python to work on through this tutorial:

python -m venv vir

For windows (Comand Prompt):

vir\Scripts\activate.bat

You should create a virtual environment for each part of the tutorial.



Each of the tutorials also have their own dependencies that need to be installed for the files to work properly. A requirements.txt file has been included in each folder and should be used for the part that they are located in.

To install:

pip install -r requirements.txt


In PART_02 you can use the script to embed your own pdfs. You can find free copies of pdfs online if you do not currently have anything you wish to embed. The script in PART_02 is capable of embedding multiple pdfs at once. Just simply dump all of your pdf files into the docs folder.

Lastly, the .env-example files need to be renamed to .env files. You will need API keys for OpenAI and Pinecone, as well as the region for your Pinecone index. A LangSmith account is recommended but not required for this tutorial. There is also an area to fill in environment variables for this in PART_03.
