# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.db.utils import IntegrityError
from django.db import transaction

from book.functions import get_book_by_book_id, get_book_by_user_trove
from .models import *


def get_receive_information_by_id(receive_information_id):
    receive_informations = ReceiveInformation.objects.filter(receive_information_id=receive_information_id)
    if receive_informations.exists():
        receive_information = receive_informations[0]
    else:
        receive_information = None
    return receive_information


def get_receive_information_by_user(user):
    receive_informations = ReceiveInformation.objects.filter(profile=user.profile)
    return receive_informations


def get_item_by_order(order):
    items = order.items.all()
    return items


def register_user(request, register_form):
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password1')
        password2 = register_form.cleaned_data.get('password2')
        phone = register_form.cleaned_data.get('phone')

        if password != password2:
            register_form.add_error('password2', "密码不一致!")
            return False

        try:
            with transaction.atomic():
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
        print("表单错误")
        return False


def modify_user_info(user, modify_user_info_form):
    if modify_user_info_form.is_valid():
        email = modify_user_info_form.cleaned_data.get('email')
        password = modify_user_info_form.cleaned_data.get('password1')
        password2 = modify_user_info_form.cleaned_data.get('password2')
        phone = modify_user_info_form.cleaned_data.get('phone')

        if password != password2:
            return False

        try:
            with transaction.atomic():
                if password is not None and password != '':
                    print('修改密码 ' + password)
                    user.set_password(password)
                    user.save()
                user.profile.email = email
                user.profile.phone = phone
                user.profile.save()
                return True
        except Exception as e:  # 已有该用户
            print(e)
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


def add_one_receive_information(user, information_dict):
    receive_informations = get_receive_information_by_user(user)
    if len(receive_informations) > 5:
        return {'result': False, 'message': '用户的收货地址最多为5条！'}
    else:
        try:
            with transaction.atomic():
                information_dict['profile'] = user.profile
                ReceiveInformation.objects.create(**information_dict)
                return {'result': True}
        except Exception as e:
            return {'result': False, 'message': str(e)}


def modify_one_receive_information(user, information_dict):
    receive_information = get_receive_information_by_id(information_dict.get('receive_information_id'))
    if receive_information is None or user.profile != receive_information.profile:
        return {'result': False, 'message': '该用户没有该收货地址！'}
    else:
        try:
            with transaction.atomic():
                receive_information.address_province = information_dict.get('address_province')
                receive_information.address_city = information_dict.get('address_city')
                receive_information.address_town = information_dict.get('address_town')
                receive_information.address_detailed = information_dict.get('address_detailed')
                receive_information.phone = information_dict.get('phone')
                receive_information.recipient = information_dict.get('recipient')
                receive_information.save()
                return {'result': True}
        except Exception as e:
            return {'result': False, 'message': str(e)}


def delete_one_receive_information(user, receive_information_id):
    receive_information = get_receive_information_by_id(receive_information_id)
    if receive_information is None or user.profile != receive_information.profile:
        return {'result': False, 'message': '该用户没有该收货地址！'}
    else:
        try:
            with transaction.atomic():
                receive_information.delete()
                return {'result': True}
        except Exception as e:
            return {'result': False, 'message': str(e)}
