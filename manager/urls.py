# -*- coding: utf-8 -*-
# 定义manager app的url

from django.conf.urls import url
from . import views

app_name = 'manager'
urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^home', views.home, name="home"),
    url(r'^look_book_detail_page/(\d+)', views.look_book_detail_page, name="look_book_detail_page"),
    url(r'^add_book_page', views.add_book_page, name="add_book_page"),
    url(r'^modify_book_page/(\d+)', views.modify_book_page, name="modify_book_page"),
    url(r'^sold_out_or_putaway/(\d+)', views.sold_out_or_putaway, name="sold_out_or_putaway"),
    url(r'^handle_orders', views.handle_orders, name="handle_orders"),
]
