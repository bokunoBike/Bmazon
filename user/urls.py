# -*- coding: utf-8 -*-
# 定义user app的url

from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^register', views.register, name="register"),
    url(r'^look_orders', views.look_orders, name="look_orders"),
    url(r'^look_shopping_cart', views.look_shopping_cart, name="look_shopping_cart"),
    url(r'^look_trove', views.look_trove, name="look_trove"),
    url(r'^handle_orders', views.handle_orders, name="handle_orders"),
]
