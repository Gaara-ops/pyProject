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

import StoreServer
from StoreServer import SnapshotManager
from StoreServer import AIStoreManager
from StoreServer import AIMiddleResult
from StoreServer import AIResult
#from StoreServer import YZAPI
from StoreServer import UserPersonalData

def AIStore(request):
    return AIStoreManager.AIStore(request)

def GetAIMiddleResult(request):
    return AIMiddleResult.GetAIMiddleResult(request)

def SubmitSnapshotResult(request):
    return SnapshotManager.SubmitSnapshotResult(request)

def GetSnapshotResult(request):
    return SnapshotManager.GetSnapshotResult(request)

def GetSnapshotList(request):
    return SnapshotManager.GetSnapshotList(request)

urlpatterns = [
    url(r'^getAi2images', AIStore),
	url(r'^AI/GetAIMiddleResult', GetAIMiddleResult),
    url(r'^AI/SubmitSnapshotResult', SubmitSnapshotResult),#上传快照结果
    url(r'^AI/GetSnapshotResult', GetSnapshotResult),#获取快照结果
    url(r'^AI/GetSnapshotList', GetSnapshotList),#获取功能列表
    url(r'^GetAIResult', AIResult.GetAIResult),#
    url(r'^AI/GetIMagesAIResult', AIResult.GetIMagesAIResult),#
    url(r'^AI/SubmitIMagesAIResult', AIResult.SubmitIMagesAIResult),#
    #yizhen
    #url(r'^oauth+', YZAPI.getToken),
    #url(r'^imageClient/getImageAuthInfo+', YZAPI.getImageAuthInfo),  #
    #url(r'^imageClient/getUserProfile+', YZAPI.GetUserProfile),  #
    #url(r'^imageClient/saveUserProfile+', YZAPI.SaveUserProfile),  #

    url(r'^yizhen-aistore/imageAi/getAi2images', AIStore),
	url(r'^storage/webs/AI/GetAIMiddleResult', GetAIMiddleResult),
    url(r'^storage/webs/AI/SubmitSnapshotResult', SubmitSnapshotResult),#上传快照结果
    url(r'^storage/webs/AI/GetSnapshotResult', GetSnapshotResult),#获取快照结果
    url(r'^storage/webs/AI/GetSnapshotList', GetSnapshotList),#获取功能列表
    url(r'^storage/webs/GetAIResult', AIResult.GetAIResult),#
    url(r'^storage/webs/AI/GetIMagesAIResult', AIResult.GetIMagesAIResult),#
    url(r'^storage/webs/AI/SubmitIMagesAIResult', AIResult.SubmitIMagesAIResult),#
    #yizhen
    #url(r'^amol-back/oauth+', YZAPI.getToken),
    #url(r'^amol-back/imageClient/getImageAuthInfo+', YZAPI.getImageAuthInfo),  #
    #url(r'^amol-back/imageClient/getUserProfile+', YZAPI.GetUserProfile),  #
    #url(r'^amol-back/imageClient/saveUserProfile+', YZAPI.SaveUserProfile),  #

    #UserPersonalData
    url(r'^storage/webs/AI/SubmitUserPersonalData', UserPersonalData.SubmitUserPersonalData),
    url(r'^storage/webs/AI/GetUserPersonalDataList', UserPersonalData.GetUserPersonalDataList),
    url(r'^storage/webs/AI/GetUserPersonalData', UserPersonalData.GetUserPersonalData),
    url(r'^storage/webs/AI/DeleteUserPersonalData', UserPersonalData.DeleteUserPersonalData),

]

