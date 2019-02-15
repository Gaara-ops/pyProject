"""MyServer URL Configuration

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
from app1 import views as learn_views

urlpatterns = [
	#http://192.168.1.68:8000/add/4/5
	path('add/<int:a>/<int:b>/', learn_views.add2, name='add2'),
	#http://192.168.1.68:8000/add/?a=4&b=5
	path('add/',learn_views.add,name='add'),
	path('',learn_views.index,name='home'),
	path('admin/', admin.site.urls),
]
