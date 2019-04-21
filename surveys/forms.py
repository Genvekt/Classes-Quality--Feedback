from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import OperationalError

from .models import USER_TYPES, ANSWER_TYPES, Courses, User, Student, Professor, CourseAndGroup, StudentGroup


def get_courses():
    # try:
    #     res = [(course.id, course.title) for course in Courses.objects.all()]
    #     return res
    # except OperationalError:
        return []


def get_users(type):
    # try:
    #     res = [(u.id, u.last_name + ' ' + u.first_name) for u in User.objects.filter(type=type).order_by('last_name')]
    #     return res
    # except OperationalError:
        return []


def get_groups():
    # try:
    #     res = [(g.id, g.name) for g in StudentGroup.objects.all()]
    #     return res
    # except OperationalError:
        return []


class Question(forms.Form):
    text = forms.CharField(label='Question text', max_length=100)
    type = forms.ChoiceField(choices=ANSWER_TYPES)

    def clean_text(self):
        return self.cleaned_data.get('text')

    def clean_type(self):
        return self.cleaned_data.get('type')


class UserName(forms.Form):
    name = forms.CharField(label='Instructor name', max_length=100)

    def clean_text(self):
        return self.cleaned_data.get("name")


class StudentGroupForm(forms.Form):
    name = forms.CharField(label='Group name', max_length=100)

    def clean_text(self):
        return self.cleaned_data.get('name')


class SurveyName(forms.Form):
    name = forms.CharField(label='Survey name', max_length=100)
    course = forms.ChoiceField(choices=get_courses())

    def clean_text(self):
        return self.cleaned_data.get('name')

    def clean_course(self):
        return self.cleaned_data.get('course')


class Survey(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(Survey, self).__init__(*args, **kwargs)

        for i, question, type in extra:
            if type == 't':
                self.fields['custom_%s' % i] = forms.CharField(label=question)
            elif type == 'r':
                choices = [(i, i) for i in range(11)]
                self.fields['custom_%s' % i] = forms.ChoiceField(label=question, choices=choices)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (int(name[7:]), value)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(label="User Type", choices=USER_TYPES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class ChooseStudent(forms.Form):
    g_id = 0
    id = forms.ChoiceField(label="Student: ", choices=get_users('s'))

    def __init__(self, *args, **kwargs):
        self.g_id = kwargs.pop('g_id')
        super(ChooseStudent, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.ChoiceField(label="Student: ", choices=get_users('s'))

    def clean_id(self):
        id = self.cleaned_data.get('id')
        try:
            Student.objects.get(user_id=id, group_id=self.g_id)
            raise ValidationError('This user is already in group')
        except Student.DoesNotExist:
            pass
        return id


class ChooseProfessor(forms.Form):
    id = forms.ChoiceField(label="Professor: ", choices=[])
    c_id = 0

    def __init__(self, *args, **kwargs):
        self.c_id = kwargs.pop('c_id')
        super(ChooseProfessor, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.ChoiceField(label="Professor: ", choices=get_users('p'))

    def clean_id(self):
        id = self.cleaned_data.get('id')
        try:
            Professor.objects.get(user_id=id, course_id=self.c_id)
            raise ValidationError('This professor is already assigned to course')
        except Professor.DoesNotExist:
            pass
        return id


class ChooseGroup(forms.Form):
    id = forms.ChoiceField(label="Group ", choices=[])
    c_id = 0

    def __init__(self, *args, **kwargs):
        self.c_id = kwargs.pop('c_id')
        super(ChooseGroup, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.ChoiceField(label="Group ", choices=get_groups())

    def clean_id(self):
        id = self.cleaned_data.get('id')
        try:
            CourseAndGroup.objects.get(group_id=id, course_id=self.c_id)
            raise ValidationError('This group is already assigned to course')
        except CourseAndGroup.DoesNotExist:
            pass
        return id

