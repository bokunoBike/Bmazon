from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import *


def get_book_file_path(instance, filename):
    book_id = instance.book.book_id
    name = instance.book.name
    return 'books/%s/%s' % (str(book_id) + name, filename)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)  # id
    name = models.CharField(max_length=50, null=False)  # 书名
    category = models.CharField(max_length=20, null=False)  # 书籍类别
    publisher = models.CharField(max_length=50, null=False)  # 出版社
    author = models.CharField(max_length=50, null=False)  # 作者
    origin_price = models.FloatField(max_length=6, null=False,
                                     validators=[validate_not_negative_number])  # 书籍价格
    stock = models.IntegerField(null=False, default=0, validators=[validate_not_negative_number])  # 书籍库存
    discount = models.DecimalField(max_length=3, decimal_places=2, max_digits=2, null=False, default=1,
                                   validators=[validate_discount])  # 书籍折扣
    sale_number = models.IntegerField(null=False, default=0, validators=[validate_not_negative_number])  # 书籍销量
    is_on_sale = models.BooleanField(null=False, default=True)  # 是否上架
    putaway_date = models.DateTimeField(null=False, auto_now_add=True)  # 上架时间

    def __str__(self):
        return str(self.name + str(self.book_id))


class BookDetail(models.Model):
    book = models.OneToOneField(Book, null=False, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to=get_book_file_path, null=True, default="img/cover/default.jpg")
    catalogue = models.FileField(upload_to=get_book_file_path, null=True)  # 书籍目录
    summary = models.FileField(upload_to=get_book_file_path, null=True)  # 书籍简介

    @receiver(post_save, sender=Book)
    def create_book_bookdetail(sender, instance, created, **kwargs):
        if created:
            BookDetail.objects.create(book=instance)

    @receiver(post_save, sender=Book)
    def save_book_bookdetail(sender, instance, **kwargs):
        instance.bookdetail.save()

    def __str__(self):
        return str(self.book)
