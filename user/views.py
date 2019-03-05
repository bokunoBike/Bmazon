from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
import urllib.parse

from .forms import *
from .functions import *
from book.functions import get_book_by_user_trove, get_books_to_page, get_book_by_book_id, \
    get_books_by_search_info, get_book_by_user_shopping_cart
from order.functions import create_item, get_orders_by_user, cancel_one_order, create_order


# 登录页面
def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            print("尝试登录")
            if user is not None:  # 登录成功
                auth.login(request, user)
                redirect_to = request.POST.get('redirect_to', reverse('user:home'))
                if redirect_to is None or redirect_to == '':
                    redirect_to = reverse('user:home')
                # print(redirect_to)
                return redirect(redirect_to)
            else:  # 登录失败
                return render(request, 'user/login.html', {'login_form': login_form, 'error_info': "用户名或密码错误！"})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        redirect_to = request.GET.get('redirect_to', reverse('user:home'))
        if redirect_to is None or redirect_to == '':
            redirect_to = reverse('user:home')
        return render(request, 'user/login.html', {'login_form': login_form, 'redirect_to': redirect_to})


# 注册
def register(request):  # 注册页面
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_user(request, register_form):  # 注册成功
            print("注册成功")
            return render(request, 'user/home.html')
        else:  # 注册失败
            print("注册失败")
            return render(request, 'user/register.html', {'register_form': register_form})
    else:  # 当正常访问时
        register_form = RegisterForm
        return render(request, 'user/register.html', {'register_form': register_form})


# 登出
def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('user:home'))


# 主页
def home(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        search_info = request.POST.get('search_info', "")
        books = get_books_by_search_info(search_info, ignore_sold_out=True)
    else:  # 正常访问
        search_info = request.GET.get("search_info", "")
        if search_info == "":
            books = get_books_by_search_info(ignore_sold_out=True)
        else:
            search_info = urllib.parse.unquote(search_info)
            books = get_books_by_search_info(search_info, ignore_sold_out=True)

    contacts = get_books_to_page(books, page=page)
    contacts.page_max_limit = contacts.number + 5
    contacts.page_min_limit = contacts.number - 5
    return render(request, 'user/home.html',
                  {'user': user, 'contacts': contacts})


def look_book_detail_page(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is None:
        return render(request, 'error.html', {'user': user, 'error_message': '暂无此书籍'})
    else:
        book.price = float('%.2f' % (float(book.discount) * book.origin_price))
        has_reserved = has_reserved_book(user, book.book_id)
        return render(request, 'user/look_book_detail_page.html',
                      {'user': user, 'book': book, 'has_reserved': has_reserved})


@login_required(login_url='user:login')
def look_orders_page(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    orders = get_orders_by_user(user)

    contacts = get_books_to_page(orders, page=page)
    return render(request, 'user/look_orders_page.html', {'user': user, 'contacts': contacts})


@login_required(login_url='user:login')
def cancel_order(request):
    user = auth.get_user(request)
    order_id = request.POST.get('order_id')
    cancel_one_order(user, order_id)
    return redirect(reverse('user:look_orders_page'))


@login_required(login_url='user:login')
def look_shopping_cart_page(request):
    user = auth.get_user(request)

    books = get_book_by_user_shopping_cart(user)[0:20]  # 限制返回最多20个
    for book in books:
        book.price = round(book.origin_price * float(book.discount), 2)
    receive_informations = get_receive_information_by_user(user)
    return render(request, 'user/look_shopping_cart_page.html',
                  {'user': user, 'books': books, 'receive_informations': receive_informations})


@login_required(login_url='user:login')
def add_book_to_shopping_cart(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is not None and book not in get_book_by_user_shopping_cart(user):
        user.profile.shopping_cart.add(book)
    return redirect(reverse('user:look_book_detail_page', args=[book_id]))


@login_required(login_url='user:login')
def drop_book_from_shopping_cart(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is not None and book in get_book_by_user_shopping_cart(user):
        user.profile.shopping_cart.remove(book)
    return redirect(reverse('user:look_shopping_cart_page'))


@require_http_methods(["POST"])
@login_required(login_url='user:login')
def shopping_cart_to_orders(request):
    user = auth.get_user(request)
    books = get_book_by_user_shopping_cart(user, ignore_sold_out=False)
    fail_items = []
    success_items = []
    for book in books:
        sale_count = int(request.POST.get(str(book.book_id), '0'))
        if sale_count <= 0:
            continue
        result = create_item(book, sale_count)
        if result.get('result', False):
            success_items.append({'book': book})
        else:
            fail_items.append({'book': book, 'fail_message': result.get('fail_message', 'error!')})

    receive_information_id = int(request.POST.get('receive_information_id', -1))
    if receive_information_id != -1:
        receive_information = get_receive_information_by_id(receive_information_id)
        address_province = receive_information.address_province
        address_city = receive_information.address_city
        address_town = receive_information.address_town
        address_detailed = receive_information.address_detailed
        phone = receive_information.phone
        recipient = receive_information.recipient

    create_dict = {'profile': user.profile, 'address_province': address_province, 'address_city': address_city,
                   'address_town': address_town,
                   'address_detailed': address_detailed, 'phone': phone, 'recipient': recipient, 'coupon': 0}
    create_order(user, success_items, create_dict=create_dict)

    # print(success_items)
    # print(fail_items)
    return render(request, 'user/purchase_result.html',
                  {'user': user, 'success_items': success_items, 'fail_items': fail_items})


@login_required(login_url='user:login')
def look_trove_page(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    books = get_book_by_user_trove(user)
    contacts = get_books_to_page(books, page=page)
    return render(request, 'user/look_trove_page.html', {'user': user, 'contacts': contacts})


@login_required(login_url='user:login')
def trove_or_cancel_trove_book(request, book_id):
    user = auth.get_user(request)
    redirect_to = request.GET.get('redirect_to')
    if redirect_to is None or redirect_to == '':
        redirect_to = reverse('user:home')
    book = get_book_by_book_id(book_id)
    if book is not None:
        if has_reserved_book(user, book_id):  # 取消收藏
            user.profile.trove_books.remove(book)
        else:  # 收藏
            user.profile.trove_books.add(book)
    return redirect(redirect_to)


@login_required(login_url='user:login')
def look_user_information_page(request):
    user = auth.get_user(request)
    profile = user.profile
    receive_informations = get_receive_information_by_user(user)
    return render(request, 'user/look_user_information_page.html',
                  {'user': user, 'profile': profile, 'receive_informations': receive_informations})


@login_required(login_url='user:login')
def modify_user_information_page(request):
    user = auth.get_user(request)
    if request.method == 'POST':
        modify_user_info_form = ModifyUserInfoForm(request.POST)
        if modify_user_info(user, modify_user_info_form):
            return redirect(reverse('user:look_user_information_page'))
        else:
            receive_informations = get_receive_information_by_user(user)
            return render(request, 'user/modify_user_information_page.html',
                          {'user': user, 'modify_user_info_form': modify_user_info_form,
                           'receive_informations': receive_informations})
    else:  # 当正常访问时
        modify_user_info_form = ModifyUserInfoForm(
            {'phone': user.profile.phone, 'email': user.profile.email})
        receive_informations = get_receive_information_by_user(user)
        return render(request, 'user/modify_user_information_page.html',
                      {'user': user, 'modify_user_info_form': modify_user_info_form,
                       'receive_informations': receive_informations})


@login_required(login_url='user:login')
def add_receive_information_page(request):
    user = auth.get_user(request)
    redirect_to = request.GET.get('redirect_to', reverse('user:home'))
    if redirect_to is None or redirect_to == '':
        redirect_to = reverse('user:home')
    if request.method == 'POST':
        receive_information_form = ReceiveInformationForm(request.POST)
        if receive_information_form.is_valid():
            address_province = receive_information_form.cleaned_data.get('address_province')
            address_city = receive_information_form.cleaned_data.get('address_city')
            address_town = receive_information_form.cleaned_data.get('address_town')
            address_detailed = receive_information_form.cleaned_data.get('address_detail')
            phone = receive_information_form.cleaned_data.get('phone')
            recipient = receive_information_form.cleaned_data.get('recipient')

            information_dict = {'address_province': address_province, 'address_city': address_city,
                                'address_town': address_town, 'address_detailed': address_detailed, 'phone': phone,
                                'recipient': recipient}
            result = add_one_receive_information(user, information_dict)

            if result.get('result', False):
                return redirect(redirect_to)
            else:
                return render(request, 'error.html', {'user': user, 'error_message': result.get('message')})
        else:
            return render(request, 'user/add_receive_information_page.html',
                          {'user': user, 'receive_information_form': receive_information_form})
    else:  # 正常访问
        receive_information_form = ReceiveInformationForm(
            {'phone': user.profile.phone, })
        return render(request, 'user/add_receive_information_page.html',
                      {'user': user, 'receive_information_form': receive_information_form, })


@require_http_methods(["POST"])
@login_required(login_url='user:login')
def delete_receive_info(request):
    user = auth.get_user(request)
    receive_information_id = request.POST.get('receive_information_id')
    receive_information = get_receive_information_by_id(receive_information_id)
    if receive_information is not None and receive_information.profile == user.profile:
        receive_information.delete()
    redirect_to = request.POST.get('redirect_to', reverse('user:home'))
    if redirect_to is None or '':
        redirect_to = reverse('user:home')
    return redirect(redirect_to)
