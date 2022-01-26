from django import forms
from .models import Post, Comment
from django.forms import TextInput, Textarea

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']
    labels = {
      'content': '답변내용',
    }

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['subject', 'description', 'content']
    widgets = {
        'subject': TextInput(attrs={
            'class':'form-control',
            'width':'100%',
        }),
        'description':Textarea(attrs={
            'class':'form-control',
            'width':'100%',
            'rows': 5,
        }),
    }
    labels = {
      'subject': '제목',
      'description': '설명',
      'content': '코드',
    }