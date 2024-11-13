from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.schema import(SystemMessage,HumanMessage,AIMessage)
from langchain.prompts import ChatPromptTemplate ,HumanMessagePromptTemplate ,SystemMessagePromptTemplate
from django.shortcuts import render
from langchain.chains import LLMChain , RetrievalQA
from langchain.document_loaders import PyPDFLoader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import  tiktoken
import pinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import ServerlessSpec
from langchain_community.vectorstores import Pinecone
import tempfile

from twisted.internet.defer import passthru

from llm.models import ChatHistory ,Session ,Index_Name
from django.http import JsonResponse


def home(request):
    session_history = Session.objects.filter(created_by=request.user).order_by('-create_at').values('group', 'title')
    indexes = Index_Name.objects.all().values('name')
    return render(request, 'streamlit.html',context={'session_history':session_history ,'indexes':indexes})

def get_chat_history(request):
    group = request.GET.get('group')
    chat_history = ChatHistory.objects.filter(session__group=group, created_by=request.user).values('question', 'answer')
    return JsonResponse({'chat_history': list(chat_history)})

class AskGPT:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4-turbo-preview',temperature=0)

    def ask_gpt(self, vector_store, question, session_id):
        retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
        # Retrieve chat history if it exists
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=retriever,
        )

        chat_history = ChatHistory.objects.filter(session_id=session_id).order_by('create_at')
        formatted_history = []
        if chat_history.exists():
            for chat in chat_history:
                formatted_history.append(f"User: {chat.question}\nAgent: {chat.answer}")
            # Joining the history in a format the agent can understand
            history_context = "\n\n".join(formatted_history)
            # Including the formatted history as context for the question
            full_prompt = f"Here is the previous conversation history:\n{history_context}\n\nUser: {question}"
        else:
            title_prompt = f"Generate a concise title (under 50 words) for the following session context:\n\n{question}"
            title = chain.run(title_prompt)
            session_obj = Session.objects.filter(group=session_id).first()
            session_obj.title=title[:50] # Ensuring title length is capped at 50 words
            session_obj.save()
            full_prompt = question  # No history available, using only the current question
        output = chain.run(full_prompt)
        return output

class UploadContentView:
    def __init__(self):
        self.pc = pinecone.Pinecone()  # Initialize Pinecone connection
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)  # Ensure correct usage of OpenAI embeddings

    def file_content(self, file):
        # Read the file bytes
        file_byte = file.read()
        # Create a temporary file to store the PDF content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_byte)  # Write byte data to the temp file
            temp_file_path = temp_file.name  # Get temp file path

        # Load content using PyPDFLoader
        loader = PyPDFLoader(temp_file_path)
        data = loader.load()
        return data

    def chunk_data(self, data):
        # Chunk data using a text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=0)
        chunks = text_splitter.split_documents(data)
        return chunks

    def embedding_cost(self, chunks):
        enc = tiktoken.encoding_for_model('text-embedding-ada-002')
        total_tokens = sum(len(enc.encode(page.page_content)) for page in chunks)
        return total_tokens / 1000 * 0.0004  # Cost calculation

    def update_embedding(self, file, index_name, namespace):
        data = self.file_content(file)
        chunks = self.chunk_data(data)
        chunks_length = len(chunks)
        embedding_cost = self.embedding_cost(chunks)
        chunk_texts = [str(chunk) for chunk in chunks]
        embeddings = self.embeddings.embed_documents(chunk_texts)
        try:
            index = self.pc.Index(index_name)
            index.upsert(
                vectors=[
                    {"id": f"chunk-{i}", "values": embedding}
                    for i, embedding in enumerate(embeddings)
                ],
                namespace=namespace
            )
            return True, chunks_length, embedding_cost
        except Exception as e:
            # Return detailed error message for easier debugging
            return False, chunks_length, embedding_cost
    def create_embedding(self, index_name):
        self.pc.create_index(
            name=index_name.lower(),
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

class Retrieve_Index:

    def fetch_all_embeddings(self,index_name):
        embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
        vector_store = Pinecone.from_existing_index(index_name, embeddings)
        return vector_store

    def delete_pinecone_index(self,index_name ,name_space=None):
        pc = pinecone.Pinecone()
        try:
            if name_space:
                index = pc.Index(index_name)
                index.delete(delete_all=True, namespace=name_space)
            else:
                pc.delete_index(index_name)
        except:
            pass


