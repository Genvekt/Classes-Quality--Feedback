from django.test import TestCase
from surveys.models import Surveys, Questions


# Create your tests here.
class DBAdditionTestCases(TestCase):
    def setUp(self):
        survey = Surveys.objects.create(name="Test survey.")
        Questions.objects.create(survey_id=survey.id, text="Q1",answer_type_id=0)
        Questions.objects.create(survey_id=survey.id, text="Q2",answer_type_id=0)

    def test_addition_is_correct(self):
        survey = Surveys.objects.get(name="Test survey.")
        questions = Questions.objects.filter(survey_id=survey.id)
        q_t = [q.text for q in questions]
        result = "false"
        if (q_t[0] == "Q1" and q_t[1] == "Q2") or (q_t[1] == "Q1" and q_t[0] == "Q2"):
            result = "true"
        self.assertEqual(result, "true")
