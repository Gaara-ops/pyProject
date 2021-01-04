"""StoreServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#coding: UTF-8
from django.conf.urls import url
#from django.contrib import admin
from django.http import HttpResponse
import json
import os
import struct
import sys

#import StoreServer
#from StoreServer import SnapshotManager
#from StoreServer import AIStoreManager
#from StoreServer import AIMiddleResult
#from StoreServer import AIResult
#from StoreServer import YZAPI
#from StoreServer import UserPersonalData
from . import Label

def Test(request):
	return ''
urlpatterns = [

    #Label
    url(r'^storage/webs/SubmitLesionsMarkResult*', Label.SubmitLesionsMarkResult),
    url(r'^storage/webs/GetLesionsMarkResult*', Label.GetLesionsMarkResult),
    url(r'^storage/webs/TestSaveChineseLanguage*', Label.TestSaveChineseLanguage),
    url(r'^storage/webs/TestGetChineseLanguage*', Label.TestGetChineseLanguage),

]

