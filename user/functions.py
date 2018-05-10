# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.db.utils import IntegrityError


def is_manager(user):
    return user.is_authenticated() and user.is_staff


def register_user(request, register_form):
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password1')
        phone = register_form.cleaned_data.get('phone')

        try:
            user = auth.User.objects.create_user(username=username, password=password, )
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
