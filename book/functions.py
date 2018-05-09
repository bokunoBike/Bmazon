# -*- coding: utf-8 -*-

import django.contrib.auth as auth

from .forms import *


def add_book(request):
    user = auth.get_user(request)
    if user is None or user.is_staff is False:
        result = {'result': 'fail', 'error_message': '管理员未登录！'}
    else:
        add_book_form = AddBookForm(request.POST)

