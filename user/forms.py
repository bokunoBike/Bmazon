# -*- coding: utf-8 -*-
# 定义:登录表单、注册表单、添加收货信息表单

from django import forms

from .validators import *


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
    username.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "用户名"})

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
    password.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "密码"})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check the format of username
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Check the format of password
        return password


class RegisterForm(forms.Form):
    """
    注册表单
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
    username.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "新用户名"})
    password1 = forms.CharField(
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
    password1.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "密码"})
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )
    password2.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "确认密码"})

    email = forms.EmailField(
        label='邮箱'
    )
    email.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "邮箱"})

    phone = forms.CharField(
        label='手机号',
        max_length=16,
    )
    phone.widget.attrs.update({'class': 'form-control form-input', 'placeholder': "手机号"})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check the format of username
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Check the format of password
        return password1

    def clean_password2(self):
        # Check the format of password
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 != password1:
            raise forms.ValidationError("密码不一致！")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile(r'^1[3578]\d{9}$')
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                '手机号码格式错误！',
            )
        return phone


class ModifyUserInfoForm(forms.Form):
    """
    修改用户信息表单
    """
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=6,
        max_length=12,
        required=False,
        error_messages={
            "min_length": "密码的长度应该在6到12个字符之间",
            "max_length": "密码的长度应该在6到12个字符之间",
        }
    )
    password2 = forms.CharField(
        label='确认密码',
        required=False,
        widget=forms.PasswordInput,
    )
    email = forms.EmailField(
        label='邮箱'
    )
    phone = forms.CharField(
        label='手机号',
        max_length=16,
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Check the format of password
        return password1

    def clean_password2(self):
        # Check the format of password
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 != password1:
            raise forms.ValidationError("密码不一致！")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile(r'^1[3578]\d{9}$')
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                '手机号码格式错误！',
            )
        return phone


class ReceiveInformationForm(forms.Form):
    """
    收货信息表单
    """
    address_province = forms.CharField(
        label='省',
        max_length=9,
        required=False,
        error_messages={
            "max_length": "超出长度",
        }
    )
    address_city = forms.CharField(
        label='市',
        max_length=7,
        required=False,
        error_messages={
            "max_length": "超出长度",
        }
    )
    address_town = forms.CharField(
        label='区',
        max_length=7,
        required=False,
        error_messages={
            "max_length": "超出长度",
        }
    )
    address_detail = forms.CharField(
        label='详细地址',
        max_length=40,
        error_messages={
            "required": "详细地址不能为空",
            "max_length": "超出长度",
        }
    )
    phone = forms.CharField(
        label='手机号',
        error_messages={
            "required": "手机号不能为空",
        }
    )
    recipient = forms.CharField(
        label='收货人',
        max_length=10,
        error_messages={
            "required": "收件人姓名不能为空",
            "max_length": "超出长度",
        }
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile(r'^1[3578]\d{9}$')
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                '手机号码格式错误！',
            )
        return phone

    def clean_address_detailed(self):
        address = self.cleaned_data.get("address")
        # Check the format of address
        return address

    def clean_recipient(self):
        recipient = self.cleaned_data.get("recipient")
        # Check the format of recipient
        return recipient
