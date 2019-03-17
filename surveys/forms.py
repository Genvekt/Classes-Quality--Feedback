
from django import forms


class Answer(forms.Form):
    answer = forms.CharField(label='answer', max_length=100)
