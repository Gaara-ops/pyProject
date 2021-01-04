"""Hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import view
from . import SnapshotManager
from . import UserPersonalData

urlpatterns = [
    #path('admin/', admin.site.urls),DownLoadAIFeedBack
	url(r'^GetUserAIInfo$',view.GetUserAIInfo),
	url(r'^SaveUserAIInfo$',view.SaveUserAIInfo),
	url(r'^GetAIResult$',view.DownLoadAIFeedBack),
	url(r'^yizhen-aistore/imageAi/getAi2images$',view.GetDataFromAIStore),
	url(r'^storage/webs/AI/GetAIMiddleResult$',view.GetAIMiddleInfo),
	url(r'^storage/webs/AI/SubmitSnapshotResult$', SnapshotManager.SubmitSnapshotResult),  # 上传快照结果
	url(r'^storage/webs/AI/GetSnapshotResult$', SnapshotManager.GetSnapshotResult),  # 获取快照结果
	url(r'^storage/webs/AI/GetSnapshotList$', SnapshotManager.GetSnapshotList),  # 获取功能列表
    #UserPersonalData
    url(r'^storage/webs/iMages/SubmitUserPersonalData', UserPersonalData.SubmitUserPersonalData),
    url(r'^storage/webs/iMages/GetUserPersonalDataList', UserPersonalData.GetUserPersonalDataList),
    url(r'^storage/webs/iMages/GetUserPersonalData', UserPersonalData.GetUserPersonalData),
    url(r'^storage/webs/iMages/DeleteUserPersonalData', UserPersonalData.DeleteUserPersonalData),
]