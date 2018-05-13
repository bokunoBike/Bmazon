# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import *


def get_book_by_book_id(book_id):
    books = Book.objects.filter(book_id=book_id)
    if books.exists():
        book = books[0]
    else:
        book = None
    return book


def get_book_by_user_trove(user):
    books = user.profile.trove_books.all()
    return books


def get_books_by_search_info_on_sale(keyword="", order_by="-sale_number"):  # 默认按销量降序
    if keyword is None or keyword == "":
        books = Book.objects.filter(is_on_sale=True).order_by(order_by)
    else:
        books = Book.objects.filter(
            Q(name__icontains=keyword) | Q(publisher__icontains=keyword) | Q(author__icontains=keyword) | Q(
                category=keyword)).order_by(order_by)
    return books


def get_books_by_search_info(keyword="", order_by="-sale_number"):  # 默认按销量降序
    if keyword is None or keyword == "":
        books = Book.objects.filter(is_on_sale=True).order_by(order_by)
    else:
        books = Book.objects.filter(
            Q(name__icontains=keyword) | Q(publisher__icontains=keyword) | Q(author__icontains=keyword) | Q(
                category=keyword)).order_by(order_by)
    return books


def get_books_to_page(books, page=1):
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


def modify_book(book_id, book_dic, book_detail_dic):
    book = get_book_by_book_id(book_id)
    if book is None:
        return False
    else:
        try:
            book.name = book_dic.get('name')
            book.publisher = book_dic.get('publisher')
            book.author = book_dic.get('author')
            book.category = book_dic.get('category')
            book.origin_price = book_dic.get('origin_price')
            book.discount = book_dic.get('discount')
            book.stock = book_dic.get('stock')
            book.save()
            if not (book_detail_dic.get('cover') is None or book_detail_dic.get('cover') == ""):
                book.bookdetail.cover = book_detail_dic.get('cover', book.bookdetail.cover)
            if not (book_detail_dic.get('catalogue') is None or book_detail_dic.get('catalogue') == ""):
                book.bookdetail.catalogue = book_detail_dic.get('catalogue', book.bookdetail.catalogue)
            if not (book_detail_dic.get('summary') is None or book_detail_dic.get('summary') == ""):
                book.bookdetail.summary = book_detail_dic.get('summary', book.bookdetail.summary)
            book.bookdetail.save()
            return True
        except Exception as e:
            print(e)
            return False
