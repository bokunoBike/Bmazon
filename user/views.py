from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.db.utils import IntegrityError

from .forms import *
from .models import *


def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:  # 登录成功
                auth.login(request, user)
                if user.is_staff:
                    return redirect(reverse('manager:home'))
                else:
                    return redirect(reverse('book:home'))
            else:
                return render(request, 'user/login.html', {'login_form': login_form})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        return render(request, 'user/login.html', {'login_form': login_form})


def register(request):  # 注册页面
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password1')
            phone = register_form.cleaned_data.get('phone')

            try:
                user = User.objects.create_user(username=username, password=password,)
                user.profile.email = email
                user.profile.phone = phone
                user.profile.save()
                auth.login(request, user)
                return render(request, 'book:home')
            except IntegrityError:  # 已有该用户
                register_form.add_error('username', "已有用户名!")
                return render(request, 'user/register.html', {'register_form': register_form})
        else:  # 未通过
            return render(request, 'user/register.html', {'register_form': register_form})
    else:  # 当正常访问时
        register_form = RegisterForm
        return render(request, 'user/register.html', {'register_form': register_form})


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('book:home'))
