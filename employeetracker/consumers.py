from channels.generic.websocket import JsonWebsocketConsumer
from llm.views import AskGPT ,Retrieve_Index
from llm.models import Session
from llm.models import Upload_Content

retrieve_index = Retrieve_Index()
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
        index_name = Upload_Content.objects.last().file_name
        vector_store = retrieve_index.fetch_embeddings(index_name)
        content = ask_gpt.ask_gpt(vector_store ,question)
        self.send(text_data=content)