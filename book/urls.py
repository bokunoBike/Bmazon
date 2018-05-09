# -*- coding: utf-8 -*-
# 定义book app的url

from django.conf.urls import url
from . import views

app_name = 'book'
urlpatterns = [
    url(r'^home', views.home, name="home"),
]
