from django.db import models

from django.db import models


class Surveys(models.Model):
    name = models.CharField(max_length=200)


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

