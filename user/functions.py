# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.db.utils import IntegrityError

from book.functions import get_book_by_book_id, get_book_by_user_trove


def register_user(request, register_form):
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password1')
        phone = register_form.cleaned_data.get('phone')

        try:
            user = User.objects.create_user(username=username, password=password, )
            user.profile.email = email
            user.profile.phone = phone
            user.profile.save()
            auth.login(request, user)
            return True
        except IntegrityError:  # 已有该用户
            register_form.add_error('username', "已有用户名!")
            return False
    else:
        return False


def has_reserved_book(user, book_id):
    book = get_book_by_book_id(book_id)
    books = get_book_by_user_trove(user)
    if book in books:
        return True
    else:
        return False
