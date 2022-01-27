from django.db import models
from datetime import datetime
from embed_video.fields import EmbedVideoField

'''
video url model
'''
class Video(models.Model):
    title = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    url = models.TextField()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-added']

'''
memo model(임시)
'''
class Memo(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

'''
vote model
'''
class Question(models.Model): 
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    def __str__(self): 
        return self.name

class Choice(models.Model):#Choice 객체 선언
    name = models.CharField(max_length=100)
    votes = models.IntegerField(default = 0)
    q = models.ForeignKey(Question, on_delete=models.CASCADE)

'''
chat model
'''
class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

'''
memo
'''
class MemoLecture(models.Model):
    text = models.TextField()