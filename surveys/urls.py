from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<a>\d+)/(?P<b>\d+)/$',  views.summ, name='sum'),
    url(r'^(?P<id>\d+)/survey_result/$',  views.survey_result, name='survey_result'),
    url(r'^(?P<id>\d+)/survey_submit/$',  views.survey_submit, name='survey_submit'),
    url(r'^(?P<id>\d+)/survey_view/$',  views.survey_view, name='survey_view'),
    path('', views.index, name='index')
]