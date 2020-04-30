from django import forms
from .models import Question, Choice


class Survey(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class Choiceform(forms.ModelForm):
    choice_text1 = forms.CharField(max_length=50, label="Choice1")
    choice_text2 = forms.CharField(max_length=50, label="Choice2")

    class Meta:
        model = Choice
        fields =['choice_text1','choice_text2']
