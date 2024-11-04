from Scripts.pywin32_postinstall import verbose
from langchain_openai import ChatOpenAI
from langchain.schema import(SystemMessage,HumanMessage,AIMessage)
from langchain.prompts import ChatPromptTemplate ,HumanMessagePromptTemplate ,SystemMessagePromptTemplate
from django.shortcuts import render
from langchain.chains import LLMChain

def home(request):
    return render(request, 'streamlit.html')

class AskGPT:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4-turbo-preview',temperature=0)

    def ask_gpt(self,question):
        prompt = ChatPromptTemplate(
            input_variables = ['content'],
            messages = [
                SystemMessage(content='you are a carreer consltant and professional resume writter . Your task is to enhance given resume and make sure it will pass ATS score more then 95% '),
                HumanMessagePromptTemplate.from_template('{question}')
            ]
        )
        chain = LLMChain(
            llm = self.llm,
            prompt = prompt,
            verbose =True
        )
        output = chain.invoke(chain)
        print(output ,"$$$$$")
        return output.content