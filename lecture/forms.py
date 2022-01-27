# from post.py

from cProfile import label
from django.forms.models import ModelForm 
from .models import Question, Choice

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