from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import *
from .functions import *


def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:  # 登录成功
                auth.login(request, user)
                return redirect(reverse('book:home'))
            else:
                return render(request, 'manager/login.html', {'login_form': login_form})
        else:
            return render(request, 'manager/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        return render(request, 'manager/login.html', {'login_form': login_form})


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('book:home'))


@user_passes_test(is_manager, login_url='manager:login')
def handle_orders(request):
    pass
