from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Answer

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse
from .models import Questions, Surveys, Submissions, AnswerTypes
from django.template import loader


def index(request):
    data_create()
    return HttpResponse("Hello, world. You're at the surveys index:, mane is: ")


def summ(request, a, b):
    c = int(a) + int(b)
    return HttpResponse("Sum is " + str(c))


def survey_result(request, id):
    try:
        submitions = Submissions.objects.filter(question__survey_id=id)
    except Submissions.DoesNotExist:
        submitions = None
    return render(request, 'survey_result.html', {'submitions': submitions})


def survey_submit(request, id):
    # if this is a POST request we need to process the form data
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Answer(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            answer = form.cleaned_data['answer']
            Submissions.objects.create(question_id=id, answer=answer)
            return HttpResponseRedirect(reverse('survey_result', args=[question.survey.id]))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Answer()
    return render(request, 'survey_submit.html', {'form': form, 'question': question})


def survey_view(request, id):
    questions = Questions.objects.filter(survey_id=id)
    survey = Surveys.objects.get(id=id)
    return render(request, 'survay_detail.html', {'questions': questions, 'survey': survey})


def data_create():
    a1 = AnswerTypes.objects.create(description='Text field')
    a2 = AnswerTypes.objects.create(description='Range from 1 to 10')

    survey = Surveys.objects.create(name='First survey ever')

    Questions.objects.create(text="Tel me your name, please", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="How do you feel?", survey_id=survey.id, answer_type_id=a2.id)
