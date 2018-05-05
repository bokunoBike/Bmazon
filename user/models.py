# coding: utf-8
# 定义模型，包括：用户扩展模型

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    phone = models.CharField(max_length=16, validators=[validate_phone])
    shopping_cart = models.ManyToManyField("book.Book", related_name='shopping_cart')
    trove_books = models.ManyToManyField("book.Book", related_name='trove_books')

    def __str__(self):
        return str(self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ReceiveInformation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    phone = models.CharField(max_length=16, validators=[validate_phone])
    recipient = models.CharField(max_length=10)

    def __str__(self):
        return str(self.profile.user.username)
