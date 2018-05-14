# -*- coding: utf-8 -*-

from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Order


def get_orders_by_user(user):
    orders = Order.objects.filter(profile=user.profile).order_by('-order_id')
    return orders


def get_orders_by_order_id(order_id):
    order = Order.objects.filter(order_id=order_id)
    return order


def get_orders_to_page(orders, page=1):
    paginator = Paginator(orders, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts


def create_order(book, user, sale_count):
    if sale_count > book.stock:
        return {'result': False, 'fail_message': '库存不足'}
    if not book.is_on_sale:
        return {'result': False, 'fail_message': '该书籍已下架'}
    try:
        with transaction.atomic():
            book.stock -= sale_count
            book.sale_number += sale_count
            book.save()
            user.profile.shopping_cart.remove(book)
            price = book.origin_price * float(book.discount)
            order_dict = {'profile': user.profile, 'book': book, 'sale_count': sale_count, 'price': price,
                          'total_fees': price * sale_count, 'status': 1}
            Order.objects.create(**order_dict)
            return {'result': True}
    except Exception as e:
        return {'result': False, 'fail_message': str(e)}


def cancel_one_order(user, order_id):
    orders = get_orders_by_user(user)
    if orders.filter(order_id=order_id).exists():
        order = orders.filter(order_id=order_id)[0]
    else:
        order = None
    if order is not None or user.is_staff:
        if order.status == 1:
            try:
                order.status = 0
                order.save()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
    else:
        return False
