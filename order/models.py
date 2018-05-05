from django.db import models

from .validators import *


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # 记录id，自动生成
    profile = models.ForeignKey("user.Profile", null=False, on_delete=models.CASCADE)  # 订单属主
    book = models.ForeignKey("book.Book", null=False, on_delete=models.PROTECT)
    book_count = models.IntegerField(null=False, default=0, validators=[validate_not_negative_number])
    price = models.DecimalField(max_length=6, decimal_places=2, max_digits=2, null=False,
                                validators=[validate_not_negative_number])  # 购买时的书籍价格
    coupon = models.DecimalField(max_length=6, decimal_places=2, max_digits=2, null=False,
                                 validators=[validate_not_negative_number])  # 购买时的书籍优惠总额
    total_fees = models.DecimalField(max_length=8, decimal_places=2, max_digits=2, null=False,
                                     validators=[validate_not_negative_number])  # 总价

    def __str__(self):
        return str(self.id)
