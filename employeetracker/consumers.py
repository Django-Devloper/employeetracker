import json
from channels.generic.websocket import JsonWebsocketConsumer
from sqlparse.engine.grouping import group, group_as

from llm.views import AskGPT
from llm.models import Session
from asgiref.sync import async_to_sync

ask_gpt =AskGPT()

class AskGPT(JsonWebsocketConsumer):
    def connect(self,):
        self.accept()
        # self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        # print(self.group_name,"RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        # async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

    def disconnect(self, code=None):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.group_name, self.channel_name)
        self.close()
    def get_or_create_session(self,session=None):
        session = Session.objects.get_or_create(session=session)
        return session

    def receive(self, text_data=None, **kwargs):
        question = text_data
        content = ask_gpt.ask_gpt(question)
        self.send(text_data=content)