from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<a>\d+)/(?P<b>\d+)/$',  views.summ, name='sum'),
    url(r'^courses_list$', views.courses_list, name='courses_list'),
    url(r'^courses_list/(?P<id>\d+)/delete/$', views.delete_course, name='delete_course'),
    url(r'^student_groups$', views.s_groups_list, name='s_groups_list'),
    url(r'^users/(?P<id>\d+)/activate/$', views.activate_user, name='activate_user'),
    url(r'^users/(?P<id>\d+)/delete/$', views.delete_user, name='delete_user'),
    url(r'^student_groups/(?P<id>\d+)/delete/$', views.s_group_delete, name='s_group_delete'),
    url(r'^student_groups/(?P<id>\d+)/$', views.s_group_info, name='s_group_info'),
    url(r'^delete_student/(?P<id>\d+)$', views.delete_student, name='delete_student'),
    url(r'^users/$', views.users_list, name='users_list'),
    url(r'^users/add/$', views.add_user, name='add_user'),
    url(r'^(?P<id>\d+)/survey_submit/$',  views.check_submitions, name='survey_submit'),
    url(r'^(?P<id>\d+)/survey_detail/$',  views.survey_detail, name='survey_detail'),
    url(r'^(?P<id>\d+)/survey_delete/$', views.survey_delete, name='survey_delete'),
    url(r'^(?P<s_id>\d+)/survey_detail/(?P<q_id>\d+)/delete$',  views.question_delete, name='question_delete'),
    url(r'^(?P<id>\d+)/course_info/$',  views.course_info, name='course_info'),
    url(r'^(?P<id>\d+)/delete_group_from_course$', views.delete_group_from_course, name='delete_g_from_c'),
    url(r'^(?P<id>\d+)/course_instructors/$',  views.course_instructors, name='course_instructors'),
    url(r'^(?P<id>\d+)/delete_prof$', views.delete_prof, name='delete_prof'),
    url(r'create_data/',  views.data_create, name='create_data'),
    path('survey_list/',  views.survey_list, name='survey_list'),
    path('survey_create/',  views.survey_create, name='survey_create'),
    path('results/', views.results, name='results'),
    path('', views.index, name='index')
]

