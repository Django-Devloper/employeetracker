from django.contrib import admin
from llm.models import Upload_Content,Session,ChatHistory
# Register your models here.

admin.site.register(Upload_Content)
admin.site.register(Session)
admin.site.register(ChatHistory)