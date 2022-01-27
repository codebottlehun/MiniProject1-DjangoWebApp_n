# from post.py

from cProfile import label
from django.forms.models import ModelForm 
from .models import Question, Choice, Video, MemoLecture

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields = ['name']

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.fields['name'].label = "Questtion"

        
class ChoiceForm(ModelForm):
    class Meta:
        model=Choice
        fields = ['q', 'name']

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.fields['name'].label = "Option"
        self.fields['q'].label="Question"

class VideoForm(ModelForm):
    class Meta:
        model=Video
        fields = ['title', 'url']

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.fields['title'].label = "Title"
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'rows': 1
        }
        self.fields['url'].label="URL"
        self.fields['url'].widget.attrs = {
            'class': 'form-control',
            'rows': 3
        }

class MemoForm(ModelForm):
    class Meta:
        model=MemoLecture
        fields=['text']
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.fields['text'].label = ""
        self.fields['text'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "write down memo and press save !",
            'rows': 20
        }