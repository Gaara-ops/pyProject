from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'learning_logs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #show all topics
    url(r'^topics/$', views.topics, name='topics'),
    #show one topic
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    #add new topic
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
]