from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<a>\d+)/(?P<b>\d+)/$',  views.summ, name='sum'),
    url(r'^(?P<id>\d+)/survey_submit/$',  views.check_submitions, name='survey_submit'),
    url(r'^(?P<id>\d+)/survey_detail/$',  views.survey_detail, name='survey_detail'),
    url(r'^(?P<id>\d+)/survey_delete/$', views.survey_delete, name='survey_delete'),
    url(r'^(?P<s_id>\d+)/survey_detail/(?P<q_id>\d+)/delete$',  views.question_delete, name='question_delete'),
    url(r'create_data/',  views.data_create, name='create_data'),
    path('survey_list/',  views.survey_list, name='survey_list'),
    path('survey_create/',  views.survey_create, name='survey_create'),
    url(r'^(?P<id>\d+)/results/$', views.results, name='results'),
    path('', views.index, name='index')
]

