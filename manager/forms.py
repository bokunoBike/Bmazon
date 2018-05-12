# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(
        label='用户名',
        min_length=6,
        max_length=14,
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名的长度应该在6到14个字符之间",
            "max_length": "用户名的长度应该在6到14个字符之间",
        }
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=6,
        max_length=12,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码的长度应该在6到12个字符之间",
            "max_length": "密码的长度应该在6到12个字符之间",
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check the format of username
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Check the format of password
        return password
