from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import *
from .models import *
from .functions import *


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
        if register_user(request, register_form):
            return render(request, 'book:home')
        else:
            return render(request, 'user/register.html', {'register_form': register_form})
    else:  # 当正常访问时
        register_form = RegisterForm
        return render(request, 'user/register.html', {'register_form': register_form})


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('book:home'))


@login_required(login_url='user:login')
def look_orders(request):
    pass


@login_required(login_url='user:login')
def look_shopping_cart(request):
    pass


@login_required(login_url='user:login')
def look_trove(request):
    pass


@user_passes_test(is_manager, login_url='user:login')
def handle_orders(request):
    pass
