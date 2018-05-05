# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import re


def validate_not_negative_number(value):
    if value < 0:
        raise ValidationError(
            '不能为负数！',
            params={'value': value},
        )


def validate_discount(value):
    if value < 0:
        raise ValidationError(
            '不能为负数！',
            params={'value': value},
        )
    elif value > 1 and value - 1.0 > 1e-6:
        raise ValidationError(
            '不能大于1！',
            params={'value': value},
        )
