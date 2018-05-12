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
        max_length=30,
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
    origin_price = forms.FloatField(
        label='原价',
        min_value=0,
        error_messages={
            "required": "原价不能为空！",
            "min_value": "不能为负数！",
        }
    )
    discount = forms.DecimalField(
        label='折扣',
        max_value=1,
        min_value=0,
        decimal_places=2,
        max_digits=2,
        validators=[validate_discount],
        error_messages={
            "max_value": "超出最大值！",
            "min_value": "不能为负数！",
        }
    )
    stock = forms.IntegerField(
        label='库存',
        min_value=0,
        error_messages={
            "min_value": "不能为负数！",
        }
    )
    cover = forms.ImageField(
        label='封面',
    )
    catalogue = forms.FileField(
        label='目录'
    )
    summary = forms.FileField(
        label='摘要'
    )


class ModifyBookForm(forms.Form):
    """
    修改书籍表单
    """
    book_id = forms.HiddenInput()
    name = forms.CharField(
        label='书名',
        max_length=30,
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
    origin_price = forms.FloatField(
        label='原价',
        min_value=0,
        error_messages={
            "required": "原价不能为空！",
            "min_value": "不能为负数！",
        }
    )
    discount = forms.DecimalField(
        label='折扣',
        max_value=1,
        min_value=0,
        decimal_places=2,
        max_digits=2,
        validators=[validate_discount],
        error_messages={
            "max_value": "超出最大值！",
            "min_value": "超出最小值！",
        }
    )
    stock = forms.IntegerField(
        label='库存',
        min_value=0,
        error_messages={
            "min_value": "不能为负数！",
        }
    )
    cover = forms.ImageField(
        label='封面',
        required=False,
    )
    catalogue = forms.FileField(
        label='目录',
        required=False,
    )
    summary = forms.FileField(
        label='摘要',
        required=False,
    )


class SearchBookForm(forms.Form):
    """
    查询书籍表单
    """
    search_info = forms.CharField(
        label='搜索书籍',
        max_length=30,
    )
    # order_by = forms.ModelChoiceField(label=u'排序', queryset=['销量', '价格', '上架时间'])
