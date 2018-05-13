from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

from .forms import *
from .models import *
from .functions import *
from book.functions import get_book_by_user_trove, get_books_to_page, get_book_by_book_id


def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:  # 登录成功
                auth.login(request, user)
                redirect_to = request.POST.get('redirect_to', reverse('book:home'))
                # print(redirect_to)
                return redirect(redirect_to)
            else:
                return render(request, 'user/login.html', {'login_form': login_form})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        redirect_to = request.GET.get('redirect_to', reverse('book:home'))
        return render(request, 'user/login.html', {'login_form': login_form, 'redirect_to': redirect_to})


def register(request):  # 注册页面
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_user(request, register_form):
            return render(request, 'book/home.html')
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
def look_trove_page(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    books = get_book_by_user_trove(user)
    contacts = get_books_to_page(books, page=page)
    return render(request, 'user/look_trove_page.html', {'user': user, 'contacts': contacts})


@login_required(login_url='user:login')
def trove_or_cancel_trove_book(request, book_id):
    user = auth.get_user(request)
    redirect_to = request.GET.get('redirect_to')
    book = get_book_by_book_id(book_id)
    if book is not None:
        if has_reserved_book(user, book_id):  # 取消收藏
            user.profile.trove_books.remove(book)
        else:  # 收藏
            user.profile.trove_books.add(book)
    return redirect(redirect_to)
