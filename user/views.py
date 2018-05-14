from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django import forms
from django.views.decorators.http import require_http_methods

from .forms import *
from .models import *
from .functions import *
from book.functions import get_book_by_user_trove, get_books_to_page, get_book_by_book_id, \
    get_books_by_search_info, get_book_by_user_shopping_cart
from order.functions import create_order, get_orders_by_user, cancel_one_order


def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:  # 登录成功
                auth.login(request, user)
                redirect_to = request.POST.get('redirect_to', reverse('user:home'))
                # print(redirect_to)
                return redirect(redirect_to)
            else:
                return render(request, 'user/login.html', {'login_form': login_form})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        redirect_to = request.GET.get('redirect_to', reverse('user:home'))
        return render(request, 'user/login.html', {'login_form': login_form, 'redirect_to': redirect_to})


def register(request):  # 注册页面
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_user(request, register_form):
            return render(request, 'user/home.html')
        else:
            return render(request, 'user/register.html', {'register_form': register_form})
    else:  # 当正常访问时
        register_form = RegisterForm
        return render(request, 'user/register.html', {'register_form': register_form})


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('user:home'))


def home(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        search_info = request.POST.get('search_info', "")
        books = get_books_by_search_info(search_info, ignore_sold_out=True)
        contacts = get_books_to_page(books, page=page)
        return render(request, 'user/home.html',
                      {'user': user, 'contacts': contacts, })
    else:  # 正常访问
        books = get_books_by_search_info(ignore_sold_out=True)
        contacts = get_books_to_page(books, page=page)
        return render(request, 'user/home.html',
                      {'user': user, 'contacts': contacts, })


def look_book_detail_page(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is None:
        return render(request, 'error.html', {'user': user, 'error_message': '暂无此书籍'})
    else:
        has_reserved = has_reserved_book(user, book.book_id)
        return render(request, 'user/look_book_detail_page.html',
                      {'user': user, 'book': book, 'has_reserved': has_reserved})


@login_required(login_url='user:login')
def look_orders_page(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    orders = get_orders_by_user(user)
    contacts = get_books_to_page(orders, page=page)
    return render(request, 'user/look_orders_page.html', {'user': user, 'contacts': contacts})


@login_required(login_url='user:login')
def cancel_order(request):
    user = auth.get_user(request)
    order_id = request.POST.get('order_id')
    cancel_one_order(user, order_id)
    return redirect(reverse('user:look_orders_page'))


@login_required(login_url='user:login')
def look_shopping_cart_page(request):
    user = auth.get_user(request)
    books = get_book_by_user_shopping_cart(user)[0:20]  # 限制返回最多20个
    for book in books:
        book.price = book.origin_price * float(book.discount)
    return render(request, 'user/look_shopping_cart_page.html', {'user': user, 'books': books})


@login_required(login_url='user:login')
def add_book_to_shopping_cart(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is not None and book not in get_book_by_user_shopping_cart(user):
        user.profile.shopping_cart.add(book)
    return redirect(reverse('user:look_book_detail_page', args=[book_id]))


@login_required(login_url='user:login')
def drop_book_from_shopping_cart(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is not None and book in get_book_by_user_shopping_cart(user):
        user.profile.shopping_cart.remove(book)
    return redirect(reverse('user:look_shopping_cart_page'))


@require_http_methods(["POST"])
@login_required(login_url='user:login')
def shopping_cart_to_orders(request):
    user = auth.get_user(request)
    books = get_book_by_user_shopping_cart(user, ignore_sold_out=False)
    fail_orders = []
    success_orders = []
    for book in books:
        sale_count = int(request.POST.get(str(book.book_id), '0'))
        if sale_count <= 0:
            continue
        result = create_order(book, user, sale_count)
        if result.get('result', False):
            success_orders.append(book)
        else:
            fail_orders.append({'book': book, 'fail_message': result.get('fail_message', 'error!')})

    return render(request, 'user/purchase_result.html',
                  {'user': user, 'success_orders': success_orders, 'fail_orders': fail_orders})


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
