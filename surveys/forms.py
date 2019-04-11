
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import OperationalError

from .models import USER_TYPES, Courses, User

def get_courses():
    try:
        res = [(course.id, course.title) for course in Courses.objects.all()]
        return res
    except OperationalError:
        return []


class Question(forms.Form):
    text = forms.CharField(label='Question text', max_length=100)

    def clean_text(self):
        return self.cleaned_data.get('text')


class SurveyName(forms.Form):
    name = forms.CharField(label='Survey name', max_length=100)
    course = forms.ChoiceField(choices=get_courses())

    def clean_text(self):
        return self.cleaned_data.get('name')

    def clean_course(self):
        return  self.cleaned_data.get('course')


class Survey(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(Survey, self).__init__(*args, **kwargs)

        for i, question in extra:
            self.fields['custom_%s' % i] = forms.CharField(label=question)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (int(name[7:]), value)


class Key(forms.Form):
    key = forms.CharField()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(label="User Type", choices=USER_TYPES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name')
