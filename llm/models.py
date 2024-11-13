from django.db import models
from employeeprofile.models import Base
# Create your models here.

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

class Index_Name(Base):
    name = models.CharField(max_length=50)

    class Meta:
        default_permissions = ('add', 'delete', 'view')

    def save(self, *args, **kwargs):
        from llm.views import UploadContentView
        upload_content = UploadContentView()
        upload_content.create_embedding(self.name)
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        from llm.views import Retrieve_Index
        retrieve_index = Retrieve_Index()
        retrieve_index.delete_pinecone_index(self.name)
        return super().delete()


    def __str__(self):
        return self.name

class Upload_Content(Base):
    index_name = models.ForeignKey(Index_Name,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    file= models.FileField(upload_to='upload_file/',null=True,blank=True)
    chunk_size = models.PositiveIntegerField(default=0 , null=True,blank=True)
    embedding_cost = models.FloatField(default=0 , null=True,blank=True)
    embedding_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            from llm.views import UploadContentView
            upload_content = UploadContentView()
            embedding_status , chunk_size , embedding_cost = upload_content.update_embedding(self.file ,self.index_name.name ,self.file_name)
            self.embedding_status =embedding_status
            self.chunk_size = chunk_size
            self.embedding_cost = embedding_cost
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        from llm.views import Retrieve_Index
        retrieve_index = Retrieve_Index()
        retrieve_index.delete_pinecone_index(self.index_name.name,self.file_name)
        return super().delete()

    def __str__(self):
        return self.file_name

