from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Answer, Survey
import datetime, time

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse
from .models import Questions, Surveys, Submissions, AnswerTypes
from django.template import loader


def index(request):
    data_create()
    return HttpResponseRedirect(reverse('survey_list'))


def summ(request, a, b):
    c = int(a) + int(b)
    return HttpResponse("Sum is " + str(c))


def survey_result(request, id):
    questions = Questions.objects.filter(survey_id=id).order_by('id')
    survey = Surveys.objects.get(id=id)
    try:

        submitions_temp = Submissions.objects.filter(question__survey_id=id)
        times = submitions_temp.order_by().values('time').distinct()
        for sub_time in times:
            print(sub_time.get('time'))
            print("\n")
        submitions = [Submissions.objects.filter(time=sub_time.get('time')).order_by('question_id') for sub_time in times]

    except Submissions.DoesNotExist:
        submitions = None
    return render(request, 'survey_result.html',{'submitions': submitions, 'questions': questions, 'survey': survey})


def survey_submit(request, id):
    survey = Surveys.objects.get(id=id)
    questions_temp = Questions.objects.filter(survey_id=id)
    questions = [[question.id, question.text] for question in questions_temp]
    form = Survey(request.POST or None, extra=questions)
    if request.method == 'POST':
        form = Survey(request.POST, extra=questions)
        if form.is_valid():
            for (question_id, answer) in form.extra_answers():

                t = datetime.datetime.now()
                sub_time = time.mktime(t.timetuple())
                Submissions.objects.create(question_id=question_id, answer=answer, time=sub_time)
            return HttpResponseRedirect(reverse('survey_result', args=[id]))

    return render(request, 'survey_submit.html', {'form': form, 'questions': questions, 'survey': survey})



# view all questions available on some exact survey
def survey_view(request, id):
    questions = Questions.objects.filter(survey_id=id)
    survey = Surveys.objects.get(id=id)
    return render(request, 'survey_detail.html', {'questions': questions, 'survey': survey})

def survey_list(request):
    surveys = Surveys.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})


def data_create():
    a1 = AnswerTypes.objects.create(description='Text field')
    a2 = AnswerTypes.objects.create(description='Range from 1 to 10')

    survey = Surveys.objects.create(name='First survey ever')

    Questions.objects.create(text="Tel me your name, please", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="How do you feel?", survey_id=survey.id, answer_type_id=a2.id)

