from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import *


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # 记录id，自动生成
    profile = models.ForeignKey("user.Profile", null=False, on_delete=models.CASCADE)  # 订单属主
    book = models.ForeignKey("book.Book", null=False, on_delete=models.PROTECT)
    sale_count = models.IntegerField(null=False, default=0, validators=[validate_not_negative_number])
    price = models.FloatField(max_length=6, null=False, default=0,
                              validators=[validate_not_negative_number])  # 购买时的书籍价格
    total_fees = models.FloatField(max_length=8, null=False, default=0, validators=[validate_not_negative_number])  # 总价
    status = models.IntegerField(null=False, default=1,
                                 validators=[
                                     validate_order_status])  # 订单的状态，0已取消，1待付款，2待处理，3待发货，4已收货，5已过期，6申请退款，7退款通过，8退款驳回
    create_date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)
