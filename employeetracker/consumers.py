import json
from channels.generic.websocket import JsonWebsocketConsumer
from llm.views import AskGPT
from llm.models import Session
ask_gpt =AskGPT()

class AskGPT(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code=None):
       self.close()

    def get_or_create_session(self,session=None):
        session = Session.objects.get_or_create(session=session)
        return session

    def receive(self, text_data=None, **kwargs):
        question = text_data
        content = ask_gpt.ask_gpt(question)
        response_from_server = json.dumps(content)
        print(response_from_server,"$$$$$$$$$$$$$$$$$$$")
        self.chat_message(response_from_server)

    def chat_message(self, event):
        self.send(text_data=event)
