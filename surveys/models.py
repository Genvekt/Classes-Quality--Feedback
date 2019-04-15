from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPES = (
        ('a', 'Administrator'),
        ('p', 'Professor'),
        ('s', 'Student'),
    )

ANSWER_TYPES = (
    ('t', 'Text'),
    ('r', 'Range')
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


class Questions(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    answer_type = models.CharField(max_length=1, choices=ANSWER_TYPES)
    text = models.CharField(max_length=200)


class Submissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    time = models.FloatField()


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
