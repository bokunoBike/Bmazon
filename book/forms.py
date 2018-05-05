# -*- coding: utf-8 -*-
# 定义:添加书籍表单、修改书籍信息表单

from django import forms

from .validators import *


class AddBookForm(forms.Form):
    """
    添加书籍表单
    """
    name = forms.CharField(
        label='书名',
        max_length=20,
        error_messages={
            "required": "书名不能为空！",
            "max_length": "超出长度！",
        }
    )
    publisher = forms.CharField(
        label='出版社',
        max_length=15,
        error_messages={
            "required": "出版社名不能为空！",
            "max_length": "超出长度！",
        }
    )
    author = forms.CharField(
        label='作者',
        max_length=20,
        error_messages={
            "required": "作者不能为空！",
            "max_length": "超出长度！",
        }
    )
    category = forms.CharField(
        label='书籍类别',
        max_length=20,
        error_messages={
            "required": "书籍类别不能为空！",
            "max_length": "超出长度！",
        }
    )
    origin_price = forms.DecimalField(
        label='原价',
        max_length=6,
        decimal_places=2,
        max_digits=2,
        validators=[validate_not_negative_number],
        error_messages={
            "required": "原价不能为空！",
            "max_length": "超出长度！",
        }
    )
    discount = forms.DecimalField(
        label='折扣',
        max_length=3,
        decimal_places=2,
        max_digits=2,
        validators=[validate_discount],
        error_messages={
            "max_length": "超出长度！",
        }
    )
    stock = forms.IntegerField(
        label='库存',
    )
    cover = forms.ImageField(
        label='封面'
    )
    catalogue = forms.Textarea(attrs={'cols': '40', 'rows': '7'})
    summary = forms.Textarea(attrs={'cols': '40', 'rows': '25'})


class ModifyBookForm(forms.Form):
    """
    修改书籍表单
    """
    name = forms.CharField(
        label='书名',
        max_length=20,
        error_messages={
            "required": "书名不能为空！",
            "max_length": "超出长度！",
        }
    )
    publisher = forms.CharField(
        label='出版社',
        max_length=15,
        error_messages={
            "required": "出版社名不能为空！",
            "max_length": "超出长度！",
        }
    )
    author = forms.CharField(
        label='作者',
        max_length=20,
        error_messages={
            "required": "作者不能为空！",
            "max_length": "超出长度！",
        }
    )
    category = forms.CharField(
        label='书籍类别',
        max_length=20,
        error_messages={
            "required": "书籍类别不能为空！",
            "max_length": "超出长度！",
        }
    )
    origin_price = forms.DecimalField(
        label='原价',
        max_length=6,
        decimal_places=2,
        max_digits=2,
        validators=[validate_not_negative_number],
        error_messages={
            "required": "原价不能为空！",
            "max_length": "超出长度！",
        }
    )
    discount = forms.DecimalField(
        label='折扣',
        max_length=3,
        decimal_places=2,
        max_digits=2,
        validators=[validate_discount],
        error_messages={
            "max_length": "超出长度！",
        }
    )
    stock = forms.IntegerField(
        label='库存',
    )
    cover = forms.ImageField(
        label='封面'
    )
    catalogue = forms.Textarea(attrs={'cols': '40', 'rows': '7'})
    summary = forms.Textarea(attrs={'cols': '40', 'rows': '25'})
