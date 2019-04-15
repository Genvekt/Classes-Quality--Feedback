from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .forms import Survey, Question, SurveyName, StudentGroupForm, Group
import datetime, time

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse
from .models import Questions, Surveys, Submissions, Courses, User, StudentGroup, CourseAndGroup
from django.template import loader


def index(request):
    if request.user.is_authenticated:
        return redirect('survey_list')
    else:
        users = User.objects.filter(type='a')
        return render(request, 'index.html', {'users': users})


def summ(request, a, b):
    c = int(a) + int(b)
    return HttpResponse("Sum is " + str(c))


def survey_create(request):
    form = SurveyName(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.clean_text()
            course = Courses.objects.get(id=form.clean_course())
            s = Surveys.objects.create(name=name, course=course)
            return HttpResponseRedirect(reverse('survey_detail', args=[s.id]))
    return render(request, 'survey_create.html', {'form': form})


def survey_delete(request, id):
    print(id)
    Surveys.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('survey_list'))


# view for question deletion
def question_delete(request, s_id, q_id):
    Questions.objects.filter(id=q_id).delete()
    return HttpResponseRedirect(reverse('survey_detail', args=[s_id]))


# view for survey page where survey may be edited
def survey_detail(request, id):
    try:
        survey = Surveys.objects.get(id=id)
    except Surveys.DoesNotExist:
        survey = None
    form = Question(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            text = form.clean_text()
            type = form.clean_type()
            Questions.objects.create(text=text, answer_type=type, survey_id=id)
            questions = Questions.objects.filter(survey_id=id)
            return HttpResponseRedirect(reverse('survey_detail', args=[id]))

    questions = Questions.objects.filter(survey_id=id)

    return render(request, 'survey_detail.html', {'form': form, 'questions': questions, 'survey': survey})


# view for survey page where user may submit answers
def check_submitions(request, id):
    subs = Submissions.objects.filter(question__survey_id=id, user_id=request.user.id)
    if(subs):
        return render(request, 'survey_submitted.html')
    else:
        return survey_submit(request, id)


def survey_submit(request, id):
    survey = Surveys.objects.get(id=id)
    questions_temp = Questions.objects.filter(survey_id=id)
    questions = [[question.id, question.text, question.answer_type] for question in questions_temp]
    form = Survey(request.POST or None, extra=questions)
    if request.method == 'POST':
        form = Survey(request.POST, extra=questions)
        if form.is_valid():
            t = datetime.datetime.now()
            for (question_id, answer) in form.extra_answers():
                sub_time = time.mktime(t.timetuple())
                Submissions.objects.create(user=request.user, question_id=question_id, answer=answer, time=sub_time)
            return HttpResponseRedirect(reverse('results', args=[id]))

    return render(request, 'survey_submit.html', {'form': form, 'questions': questions, 'survey': survey})


# view for page of all surveys
def survey_list(request):
    if request.user.is_authenticated:
        surveys = Surveys.objects.all()
        return render(request, 'survey_list.html', {'surveys': surveys})
    else:
        return redirect('index')


# temp view before survey creation constructor is developed
def data_create(request):
    ph = Courses.objects.create(title="Physics")
    net = Courses.objects.create(title='Networks')
    survey = Surveys.objects.create(name='Networks - Course feedback', course=net)

    User.objects.create(
        username='admin',
        password=make_password('adminpass', salt=None, hasher='default'),
        email='admin@mail.ru',
        type='a',
        is_active=True,
        is_staff=True,
        first_name='Kek',
        last_name='Dolgoborodov'
    )
    Questions.objects.create(text="Lectures", survey_id=survey.id, answer_type='r')
    Questions.objects.create(text="Tutorials", survey_id=survey.id, answer_type='t')
    Questions.objects.create(text="Labs (please, write name of your TA)", survey_id=survey.id, answer_type='r')
    Questions.objects.create(text="Comments", survey_id=survey.id, answer_type='r')

    survey = Surveys.objects.create(name='Physics - Course feedback', course=ph)
    Questions.objects.create(text="How do you like lectures? ", survey_id=survey.id, answer_type='r')
    Questions.objects.create(text="How to improve them?", survey_id=survey.id,
                             answer_type='t')
    Questions.objects.create(text="How do you like tutorials? ", survey_id=survey.id, answer_type='r')
    Questions.objects.create(text="How to improve them?", survey_id=survey.id,
                             answer_type='t')
    Questions.objects.create(text="How do you like labs? ", survey_id=survey.id, answer_type='r')
    Questions.objects.create(text="How to improve them?", survey_id=survey.id,
                             answer_type='t')

    return render(request, 'create_data.html')


# one more view to present all submissions on specified survey
def results(request, id):
    questions = Questions.objects.filter(survey_id=id).order_by('id')
    survey = Surveys.objects.get(id=id)
    try:
        submitions_temp = Submissions.objects.filter(question__survey_id=id)
        times = submitions_temp.order_by().values('time').distinct()
        submitions = [[Submissions.objects.filter(time=sub_time.get('time')).order_by('question_id')] for
                      sub_time in times]
        for s in submitions:
            s.append(s[0][:1].get().user)
    except Submissions.DoesNotExist:
        submitions = None
    return render(request, 'survey_result.html',
                  {'submitions': submitions, 'questions': questions, 'survey': survey})


def admin_board(request):
    return render(request, 'administrative/admin_board.html')


# Courses

def courses_list(request):
    course = Courses.objects.all().order_by('title')

    return render(request, 'administrative/courses_list.html', {'courses': course})


def course_info(request, id):
    course = Courses.objects.get(id=id)
    form = Group(request.POST or None)
    groups = CourseAndGroup.objects.filter(course=Courses.objects.get(id=id))
    if request.method == 'POST':
        if form.is_valid():
            name = form.clean_text()
            if len(CourseAndGroup.objects.filter(group=StudentGroup.objects.get(name=name),
                                                 course=Courses.objects.get(id=id))) == 0:
                CourseAndGroup.objects.create(group=StudentGroup.objects.get(name=name),
                                              course=Courses.objects.get(id=id))
            return HttpResponseRedirect(reverse('course_info', args=[id]))
    return render(request, 'courses/course_info.html', {'course': course, "groups": groups, "form": form})


def course_instructors(request, id):
    return render(request, 'courses/course_instructors_edit.html')


def s_groups_list(request):
    groups = StudentGroup.objects.all().order_by('name')
    form = StudentGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.clean_text()
            StudentGroup.objects.create(name=name)
            return HttpResponseRedirect(reverse('s_groups_list'))
    return render(request, 'administrative/s_groups_list.html', {'groups': groups, 'form': form})


def s_group_delete(request, id):
    StudentGroup.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('s_groups_list'))


def new_users_list(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'administrative/new_users_list.html', {'users': users})


def activate_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('new_users_list'))


def delete_user(request, id):
    User.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('new_users_list'))
