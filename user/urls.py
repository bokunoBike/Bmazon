# -*- coding: utf-8 -*-
# 定义user app的url

from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^register', views.register, name="register"),
    url(r'^home', views.home, name="home"),
    url(r'^look_book_detail_page/(\d+)', views.look_book_detail_page, name="look_book_detail_page"),
    url(r'^look_orders', views.look_orders, name="look_orders"),
    url(r'^look_shopping_cart', views.look_shopping_cart, name="look_shopping_cart"),
    url(r'^look_trove_page', views.look_trove_page, name="look_trove_page"),
    url(r'^trove_or_cancel_trove_book/(\d+)', views.trove_or_cancel_trove_book, name="trove_or_cancel_trove_book"),
]
