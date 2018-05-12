# -*- coding: utf-8 -*-
# 定义manager app的url

from django.conf.urls import url
from . import views

app_name = 'manager'
urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^handle_orders', views.handle_orders, name="handle_orders"),
]
