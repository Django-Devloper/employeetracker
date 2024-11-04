from django.db import models
from employeeprofile.models import Base
# Create your models here.
from datetime import datetime

class Session(Base):
    group = models.CharField(max_length=50)

    def save(self,*args):
        self.group= datetime.now().strftime("%Y%m%d%H%M%S")
        return super().save(*args)

    def __str__(self):
        return self.group

class ChatHistory(Base):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    question = models.TextField(max_length=5000)
    answer = models.TextField(max_length=30000)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title