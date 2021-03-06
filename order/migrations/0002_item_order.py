# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-14 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import order.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_profile_receiveinformation'),
        ('book', '0002_book_bookdetail'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('sale_count', models.IntegerField(default=0, validators=[order.validators.validate_not_negative_number])),
                ('price', models.FloatField(default=0, max_length=6, validators=[order.validators.validate_not_negative_number])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('coupon', models.IntegerField(default=0, validators=[order.validators.validate_not_negative_number])),
                ('total_fees', models.FloatField(default=0, max_length=8, validators=[order.validators.validate_not_negative_number])),
                ('address_province', models.CharField(default='暂无省份', max_length=9)),
                ('address_city', models.CharField(default='暂无城市', max_length=10)),
                ('address_town', models.CharField(default='暂无城区', max_length=10)),
                ('address_detailed', models.CharField(default='暂无详细地址', max_length=40, null=True)),
                ('phone', models.CharField(max_length=16, validators=[order.validators.validate_phone])),
                ('recipient', models.CharField(max_length=10)),
                ('status', models.IntegerField(default=1, validators=[order.validators.validate_order_status])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('items', models.ManyToManyField(related_name='items', to='order.Item')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile')),
            ],
        ),
    ]
