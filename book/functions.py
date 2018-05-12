# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import *


def get_books_by_search_info(keyword="", order_by="-sale_number"):  # 默认按销量降序
    if keyword is None or keyword == "":
        books = Book.objects.all().order_by(order_by)
    else:
        books = Book.objects.filter(
            Q(name__icontains=keyword) | Q(publisher__icontains=keyword) | Q(author__icontains=keyword) | Q(
                category=keyword)).order_by(order_by)
    return books


def get_books_by_search_info_to_page(keyword="", order_by="-sale_number", page=1):
    books = get_books_by_search_info(keyword, order_by)
    paginator = Paginator(books, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts


def add_one_book(book_dic, book_detail_dic):
    try:
        book = Book.objects.create(**book_dic)
        book_detail = book.bookdetail
        book_detail.cover = book_detail_dic.get('cover')
        book_detail.catalogue = book_detail_dic.get('catalogue')
        book_detail.summary = book_detail_dic.get('summary')
        book_detail.save()
        print('添加书籍 ' + book.name + ' 成功！')
        return True
    except Exception as e:
        print(e)
        return False
