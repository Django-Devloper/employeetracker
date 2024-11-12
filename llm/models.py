from django.db import models
from employeeprofile.models import Base
# Create your models here.
from datetime import datetime

class Session(Base):
    group = models.CharField(max_length=50)
    title = models.CharField(max_length=100,default='title')

    def __str__(self):
        return self.group

class ChatHistory(Base):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    question = models.TextField(max_length=5000)
    answer = models.TextField(max_length=30000)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.session)

class Upload_Content(Base):
    file_name = models.CharField(max_length=100)
    file= models.FileField(upload_to='upload_file/',null=True,blank=True)
    chunk_size = models.PositiveIntegerField(default=0 , null=True,blank=True)
    embedding_cost = models.FloatField(default=0 , null=True,blank=True)
    embedding_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from llm.views import Upload_Content_View
        upload_content = Upload_Content_View(self.file)
        embedding_status , chunk_size , embedding_cost = upload_content.create_embedding(self.file_name)
        self.embedding_status =embedding_status
        self.chunk_size = chunk_size
        self.embedding_cost = embedding_cost
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

