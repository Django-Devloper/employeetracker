from langchain_openai import ChatOpenAI
from langchain.schema import(SystemMessage,HumanMessage,AIMessage)
from langchain.prompts import ChatPromptTemplate ,HumanMessagePromptTemplate ,SystemMessagePromptTemplate
from django.shortcuts import render
from langchain.chains import LLMChain
from langchain.document_loaders import PyPDFLoader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import  tiktoken
import pinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import ServerlessSpec
from langchain_community.vectorstores import Pinecone
from io import BytesIO
from django.core.files.base import ContentFile
import tempfile
import PyPDF2
from langchain.schema import Document  # Import Document from langchain


def home(request):
    return render(request, 'streamlit.html')

class AskGPT:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4-turbo-preview',temperature=0)

    def ask_gpt(self,question):
        prompt = ChatPromptTemplate(
            input_variables = [question],
            messages = [
                SystemMessage(content='you are general purpose chat bot '),
                HumanMessagePromptTemplate.from_template('{question}')
            ]
        )
        chain = LLMChain(
            llm = self.llm,
            prompt = prompt,
            verbose =True
        )
        output = chain.run({'question':question})
        return output

class Upload_Content_View:
    def __init__(self , file):
        self.file = file

    def file_content(self):
        # Read the file bytes
        file_byte = self.file.read()
        # Create a temporary file to store the PDF content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_byte)  # Write the byte data to the temp file
            temp_file_path = temp_file.name  # Get the temp file path

        # Pass the temp file path to PyPDFLoader
        loader = PyPDFLoader(temp_file_path)
        data = loader.load()
        return data

    def chunk_data(self,data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=0)
        chunks = text_splitter.split_documents(data)
        return chunks

    def embedding_cost(self,chunks):
        enc = tiktoken.encoding_for_model('text-embedding-ada-002')
        total_token = sum(len(enc.encode(page.page_content)) for page in chunks)
        return total_token/1000*0.0004

    def create_embedding(self,index_name):
        data = self.file_content()
        chunks = self.chunk_data(data)
        chunks_length = len(chunks)
        embedding_cost = self.embedding_cost(chunks)
        pc = pinecone.Pinecone()
        embeddings = OpenAIEmbeddings(model = 'text-embedding-3-small', dimensions = 1536)
        pc.create_index(
            name=index_name.lower(),
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        try:
            Pinecone.from_documents(chunks,embeddings ,index_name=index_name)
            return True ,chunks_length , embedding_cost
        except Exception as e:
            return False ,chunks_length , embedding_cost

    def fetch_embeddings(self,index_name):
        pc = pinecone.Pinecone()
        embeddings = OpenAIEmbeddings(model = 'text-embedding-3-small', dimension = 1536)
        if index_name in pc.list_indexes().names():
            vector_store = Pinecone.from_existing_index(index_name, embeddings)
            return vector_store

    def delete_pinecone_index(self,index_name):
        pc = pinecone.Pinecone()
        pc.delete_index(index_name)

