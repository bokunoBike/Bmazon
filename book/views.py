from django.shortcuts import render

import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .forms import *
from .models import *


def is_manager(user):
    return user.is_authenticated() and user.is_staff


@require_http_methods(["POST"])
@user_passes_test(is_manager, login_url='/login/login')
def add_book(request):
    add_book_form = AddBookForm(request.POST)
    if add_book_form.is_valid():
        book_name = add_book_form.cleaned_data.get('name')
        publisher = add_book_form.cleaned_data.get('publisher')
        author = add_book_form.cleaned_data.get('author')
        category = add_book_form.cleaned_data.get('category')
        origin_price = add_book_form.cleaned_data.get('origin_price')
        discount = add_book_form.cleaned_data.get('discount')
        stock = add_book_form.cleaned_data.get('stock')
        cover = add_book_form.cleaned_data.get('cover')
        catalogue = add_book_form.cleaned_data.get('catalogue')
        summary = add_book_form.cleaned_data.get('summary')

        dic = {'book_name': book_name, 'publisher': publisher, 'author': author, 'category': category,
               'origin_price': origin_price, 'discount': discount, 'stock': stock, }
        try:
            book = Book.objects.create(**dic)
            book_detail = book.bookdetail
            book_detail.cover = cover
            book_detail.catalogue = catalogue
            book_detail.summary = summary
            book_detail.save()
            result = {'result': 1}
        except Exception as e:
            result = {'result': 0, 'error_message': e}

    else:
        result = {'result': 0, 'error_message': '表格内容有误'}
    return result


def modify_book(request):
    modify_book_form = ModifyBookForm(request.POST)
    if modify_book_form.is_valid():
        book_name = modify_book_form.cleaned_data.get('name')
        publisher = modify_book_form.cleaned_data.get('publisher')
        author = modify_book_form.cleaned_data.get('author')
        category = modify_book_form.cleaned_data.get('category')
        origin_price = modify_book_form.cleaned_data.get('origin_price')
        discount = modify_book_form.cleaned_data.get('discount')
        stock = modify_book_form.cleaned_data.get('stock')
        cover = modify_book_form.cleaned_data.get('cover')
        catalogue = modify_book_form.cleaned_data.get('catalogue')
        summary = modify_book_form.cleaned_data.get('summary')

        dic = {'book_name': book_name, 'publisher': publisher, 'author': author, 'category': category,
               'origin_price': origin_price, 'discount': discount, 'stock': stock, }
        try:
            book = Book.objects.save(**dic)
            book_detail = book.bookdetail
            book_detail.cover = cover
            book_detail.catalogue = catalogue
            book_detail.summary = summary
            book_detail.save()
            result = {'result': 1}
        except Exception as e:
            result = {'result': 0, 'error_message': e}

    else:
        result = {'result': 0, 'error_message': '表格内容有误'}
    return result


def home(request):
    user = auth.get_user(request)
    books = get_books_by_search_info()
    return render(request, 'book/home.html', {'user': user, 'books': books})
