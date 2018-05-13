from django.shortcuts import render

import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files import File

from .forms import *
from .models import *
from .functions import *
from manager.functions import is_manager


@user_passes_test(is_manager, login_url='manager:login')
def add_book_page(request):
    user = auth.get_user(request)
    if request.method == 'POST':
        add_book_form = AddBookForm(request.POST, request.FILES)
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

            book_dic = {'name': book_name, 'publisher': publisher, 'author': author, 'category': category,
                        'origin_price': origin_price, 'discount': discount, 'stock': stock}
            book_detail_dic = {'cover': cover, 'catalogue': catalogue, 'summary': summary}

            result = add_one_book(book_dic, book_detail_dic)
            if result:
                return render(request, 'book/add_book_successfully.html', {'user': user})
            else:
                return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:  # 表单出错
            return render(request, 'book/add_book_page.html', {'user': user, 'add_book_form': add_book_form})
    else:  # 当正常访问时
        add_book_form = AddBookForm
        return render(request, 'book/add_book_page.html', {'user': user, 'add_book_form': add_book_form})


@user_passes_test(is_manager, login_url='manager:login')
def modify_book_page(request):
    user = auth.get_user(request)
    book_id = request.GET.get('book_id')
    if request.method == 'POST':
        modify_book_form = ModifyBookForm(request.POST, request.FILES)
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

            book_dic = {'name': book_name, 'publisher': publisher, 'author': author, 'category': category,
                        'origin_price': origin_price, 'discount': discount, 'stock': stock}
            book_detail_dic = {'cover': cover, 'catalogue': catalogue, 'summary': summary}

            result = modify_book(book_id, book_dic, book_detail_dic)
            if result:
                return render(request, 'book/modify_book_successfully.html', {'user': user, 'book_id': book_id})
            else:
                return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:  # 表单出错
            return render(request, 'book/modify_book_page.html', {'user': user, 'modify_book_form': modify_book_form})
    else:  # 当正常访问时
        book = get_book_by_book_id(book_id)
        if book is None:
            return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:
            modify_book_form = ModifyBookForm(
                {'book_id': book.book_id, 'name': book.name, 'publisher': book.publisher, 'author': book.author, 'category': book.category,
                 'origin_price': book.origin_price, 'discount': book.discount, 'stock': book.stock,
                 'cover': book.bookdetail.cover,
                 'catalogue': book.bookdetail.catalogue, 'summary': book.bookdetail.summary})
            return render(request, 'book/modify_book_page.html', {'user': user, 'modify_book_form': modify_book_form})


def home(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        search_book_form = SearchBookForm(request.POST)
        if search_book_form.is_valid():
            search_info = search_book_form.cleaned_data.get('search_info')
            books = get_books_by_search_info(search_info)
            contacts = get_books_to_page(books, page=page)
            return render(request, 'book/home.html',
                          {'user': user, 'search_book_form': search_book_form, 'contacts': contacts})
    else:  # 正常访问
        search_book_form = SearchBookForm
        books = get_books_by_search_info()
        contacts = get_books_to_page(books, page=page)
        return render(request, 'book/home.html',
                      {'user': user, 'search_book_form': search_book_form, 'contacts': contacts,})


def look_book_detail_page(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is None:
        return render(request, 'error.html', {'user': user, 'error_message': '暂无此书籍'})
    else:
        return render(request, 'book/look_book_detail_page.html', {'user': user, 'book': book})
