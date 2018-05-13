# -*- coding: utf-8 -*-
# 定义book app的url

from django.conf.urls import url
from . import views

app_name = 'book'
urlpatterns = [
    url(r'^home', views.home, name="home"),
    url(r'^look_book_detail_page/(\d+)', views.look_book_detail_page, name="look_book_detail_page"),
]
