# -*- coding: utf-8 -*-
# 定义book app的url

from django.conf.urls import url
from . import views

app_name = 'book'
urlpatterns = [
    url(r'^home', views.home, name="home"),
    url(r'^add_book_page', views.add_book_page, name="add_book_page"),
    url(r'^look_book_detail_page', views.look_book_detail_page, name="look_book_detail_page"),
]
