# -*- coding: utf-8 -*-

from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *


def get_orders_by_user(user):
    orders = Order.objects.filter(profile=user.profile).order_by('-order_id')
    return orders


def get_orders_by_order_id(order_id):
    orders = Order.objects.filter(order_id=order_id)
    if orders.exists():
        order = orders[0]
    else:
        order = None
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


def get_item_by_id(item_id):
    items = Item.objects.filter(item_id=item_id)
    if items.exists():
        item = items[0]
    else:
        item = None
    return item


def create_item(book, sale_count):
    if sale_count > book.stock:
        return {'result': False, 'fail_message': '库存不足'}
    if not book.is_on_sale:
        return {'result': False, 'fail_message': '该书籍已下架'}
    try:
        with transaction.atomic():
            book.stock -= sale_count
            book.sale_number += sale_count
            book.save()
            price = book.origin_price * float(book.discount)
            item_dict = {'book': book, 'sale_count': sale_count, 'price': price}
            item = Item.objects.create(**item_dict)
            return {'result': True, 'item_id': item.item_id}
    except Exception as e:
        return {'result': False, 'fail_message': str(e)}


def create_order(user, success_items, create_dict):
    if len(success_items) == 0:
        return False
    else:
        try:
            with transaction.atomic():
                order = Order.objects.create(**create_dict)
                total_fees = 0
                for item_id in success_items:
                    item = get_item_by_id(item_id)
                    order.items.add(item)
                    user.profile.shopping_cart.remove(item.book)
                    total_fees += item.price * item.sale_count
                total_fees -= order.coupon
                order.save()
                return True
        except Exception as e:
            print(e)
            return False


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
