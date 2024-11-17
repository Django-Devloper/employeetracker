from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from llm.views import AskGPT, Retrieve_Index
from llm.models import Session, ChatHistory, Upload_Content
from asgiref.sync import sync_to_async

ask_gpt = AskGPT()

class AskGPTConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.user = self.scope["user"]

    async def disconnect(self, code=None):
        await self.close()

    async def get_or_create_session(self, session=None):
        session_obj, created = await sync_to_async(Session.objects.get_or_create)(
            group=session, created_by=self.user
        )
        return session_obj

    async def create_chat_history(self, session_id, question, answer):
        await sync_to_async(ChatHistory.objects.create)(
            session=session_id, question=question, answer=answer, created_by=self.user
        )
        return await sync_to_async(list)(
            ChatHistory.objects.filter(session=session_id).values('question', 'answer')
        )

    async def session_history(self):
        return await sync_to_async(list)(Session.objects.filter(created_by=self.user).order_by('-create_at').values('group','title'))

    async def receive(self, text_data=None, **kwargs):
        data = json.loads(text_data)
        if text_data is not None:
            question = data.get('question')  # Access 'question'
            index_name = data.get('index')  # Access 'index'
            session_obj = await self.get_or_create_session(self.group_name)
            session_id = session_obj
            retrieve_index = Retrieve_Index(index_name)
            vector_store = await sync_to_async(retrieve_index.fetch_all_embeddings)()
            content = await sync_to_async(ask_gpt.ask_gpt)(vector_store, question, session_id)
            chats = await self.create_chat_history(session_id, question, content)
            chats = list(chats)
            session_history  = await self.session_history()
            session_history = list(session_history)
            message = {'chats':chats , 'session_history':session_history}
            await self.send_json(message)
