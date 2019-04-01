from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Survey, Question, Key
import datetime, time

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse
from .models import Questions, Surveys, Submissions, AnswerTypes, SurveyKeys
from django.template import loader


def index(request):
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
        submitions = [Submissions.objects.filter(time=sub_time.get('time')).order_by('question_id') for sub_time in
                      times]

    except Submissions.DoesNotExist:
        submitions = None
    return render(request, 'survey_result.html', {'submitions': submitions, 'questions': questions, 'survey': survey})


def survey_create(request):
    pass
# TODO Add survey creation operation with data from form and redirect to new survey_detail page


def question_delete(request,s_id,q_id):
    Questions.objects.filter(id=q_id).delete()
    return HttpResponseRedirect(reverse('survey_detail', args=[s_id]))


def survey_detail(request, id):
    try:
        survey = Surveys.objects.get(id=id)
    except Surveys.DoesNotExist:
        survey = None
    form = Question(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            text = form.clean_text()
            Questions.objects.create(text=text, answer_type_id=1, survey_id=id)
            questions = Questions.objects.filter(survey_id=id)
            return HttpResponseRedirect(reverse('survey_detail', args=[id]))

    questions = Questions.objects.filter(survey_id=id)

    return render(request, 'survey_detail.html', {'form': form, 'questions': questions, 'survey': survey})


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


def survey_list(request):
    surveys = Surveys.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})


def data_create(request):
    a1 = AnswerTypes.objects.create(description='Text field')
    a2 = AnswerTypes.objects.create(description='Range from 1 to 10')

    survey = Surveys.objects.create(name='Networks - Course feedback')

    Questions.objects.create(text="Lectures", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="Tutorials", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="Labs (please, write name of your TA)", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="Comments", survey_id=survey.id, answer_type_id=a2.id)

    SurveyKeys.objects.create(survey_id=survey.id, key='123')

    survey = Surveys.objects.create(name='Physics - Course feedback')
    Questions.objects.create(text="Do you like lectures? (Yes/No)", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="If your answer is 'no', how to improve them?", survey_id=survey.id,
                             answer_type_id=a1.id)
    Questions.objects.create(text="Do you like tutorials? (Yes/No)", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="If your answer is 'no', how to improve them?", survey_id=survey.id,
                             answer_type_id=a2.id)
    Questions.objects.create(text="Do you like labs? (Yes/No)", survey_id=survey.id, answer_type_id=a1.id)
    Questions.objects.create(text="If your answer is 'no', how to improve them?", survey_id=survey.id,
                             answer_type_id=a1.id)

    SurveyKeys.objects.create(survey_id=survey.id, key='444')
    return render(request, 'create_data.html')


def results(request, id):
    if request.method == 'POST':
        form = Key(request.POST)
        if form.is_valid():
            k = form.cleaned_data.get('key')
            key = SurveyKeys.objects.get(survey_id=id)
            if k == key:
                questions = Questions.objects.filter(survey_id=id).order_by('id')
                survey = Surveys.objects.get(id=id)
                try:

                    submitions_temp = Submissions.objects.filter(question__survey_id=id)
                    times = submitions_temp.order_by().values('time').distinct()
                    for sub_time in times:
                        print(sub_time.get('time'))
                        print("\n")
                    submitions = [Submissions.objects.filter(time=sub_time.get('time')).order_by('question_id') for
                                  sub_time in
                                  times]

                except Submissions.DoesNotExist:
                    submitions = None
                return render(request, 'survey_result.html',
                              {'submitions': submitions, 'questions': questions, 'survey': survey})
            else:
                return render(request, 'results.html', {'id': id})

    return render(request, 'results.html', {'id': id})



