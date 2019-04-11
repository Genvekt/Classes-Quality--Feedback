from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPES = (
        ('a', 'Administrator'),
        ('p', 'Professor'),
        ('s', 'Student'),
    )


class User(AbstractUser):
    type = models.CharField(max_length=1, choices=USER_TYPES, blank=True, default='s')

    class Meta:
        permissions = (
            ("manage_users", "Can manage users"),
            ("add_survey", "Can add survey"),
            ("delete_survey", "Can delete survey"),
            ("modify_survey", "Can modify survey"),
            ("view_survey_result", "Can view survey result"),
            ("take_survey", "Can answer survey questions")
        )


class Courses(models.Model):
    title = models.CharField(max_length=100)


class Surveys(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


# 0 = text field
# 1 = range from 1 to 10
class AnswerTypes(models.Model):
    description = models.CharField(max_length=100)


class Questions(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    answer_type = models.ForeignKey(AnswerTypes, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)


class Submissions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    time = models.FloatField()


class SurveyKeys(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    key = models.IntegerField()


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)


class CourseAndGroup(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)


class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

