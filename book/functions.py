# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.db.models import Q

from .forms import *
from .models import *


def get_books_by_search_info(keyword="", order_by="-sale_number"):  # 默认按销量降序
    if keyword is None or keyword == "":
        books = Book.objects.all().order_by(order_by)
    else:
        books = Book.objects.filter(
            Q(name_icontains=keyword) | Q(publisher_icontains=keyword) | Q(author_icontains=keyword) | Q(
                category=keyword)).order_by(order_by)
    return books


def add_book(request):
    user = auth.get_user(request)
    if user is None or user.is_staff is False:
        result = {'result': 'fail', 'error_message': '管理员未登录！'}
    else:
        add_book_form = AddBookForm(request.POST)

