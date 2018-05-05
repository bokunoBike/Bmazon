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
