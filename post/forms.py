from django import forms
from .models import Post, Comment
from django.forms import CharField, TextInput, Textarea

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['description', 'content']
    labels = {
      'description': '코드 설명',
      'content': '코드 수정',
    }

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['subject', 'description', 'content', 'tags']
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
      'tags':'태그',
    }