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
        print(output ,"$$$$$")
        return output