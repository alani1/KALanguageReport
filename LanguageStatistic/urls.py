from django.conf.urls import patterns, url

from LanguageStatistic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^exercises/(?P<slug>.*)$', views.ExerciseList, name='ExerciseList'),
    url(r'^data/(?P<lang>.+)$', views.StatisticData, name='StatisticData'),
)