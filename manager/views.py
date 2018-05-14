from django.shortcuts import render, redirect, reverse
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import *
from .functions import *
from book.forms import AddBookForm, ModifyBookForm
from book.functions import add_one_book, modify_book, get_book_by_book_id, get_books_by_search_info, get_books_to_page


def login(request):  # 登录页面
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:  # 登录成功
                auth.login(request, user)
                redirect_to = request.POST.get('redirect_to', reverse('manager:home'))
                return redirect(redirect_to)
            else:
                return render(request, 'manager/login.html', {'login_form': login_form})
        else:
            return render(request, 'manager/login.html', {'login_form': login_form})
    else:  # 正常访问
        login_form = LoginForm
        redirect_to = request.GET.get('redirect_to', reverse('manager:home'))
        return render(request, 'manager/login.html', {'login_form': login_form, 'redirect_to': redirect_to})


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('manager:home'))


@user_passes_test(is_manager, login_url='manager:login')
def home(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        search_info = request.POST.get('search_info', "")
        books = get_books_by_search_info(search_info)
        contacts = get_books_to_page(books, page=page)
        return render(request, 'manager/home.html',
                      {'user': user, 'contacts': contacts, })
    else:  # 正常访问
        books = get_books_by_search_info()
        contacts = get_books_to_page(books, page=page)
        return render(request, 'manager/home.html',
                      {'user': user, 'contacts': contacts, })


@user_passes_test(is_manager, login_url='manager:login')
def look_book_detail_page(request, book_id):
    user = auth.get_user(request)
    book = get_book_by_book_id(book_id)
    if book is None:
        return render(request, 'error.html', {'user': user, 'error_message': '暂无此书籍'})
    else:
        return render(request, 'manager/look_book_detail_page.html',
                      {'user': user, 'book': book})


@user_passes_test(is_manager, login_url='manager:login')
def add_book_page(request):
    user = auth.get_user(request)
    if request.method == 'POST':
        add_book_form = AddBookForm(request.POST, request.FILES)
        if add_book_form.is_valid():
            book_name = add_book_form.cleaned_data.get('name')
            publisher = add_book_form.cleaned_data.get('publisher')
            author = add_book_form.cleaned_data.get('author')
            category = add_book_form.cleaned_data.get('category')
            origin_price = add_book_form.cleaned_data.get('origin_price')
            discount = add_book_form.cleaned_data.get('discount')
            stock = add_book_form.cleaned_data.get('stock')
            cover = add_book_form.cleaned_data.get('cover')
            catalogue = add_book_form.cleaned_data.get('catalogue')
            summary = add_book_form.cleaned_data.get('summary')

            book_dic = {'name': book_name, 'publisher': publisher, 'author': author, 'category': category,
                        'origin_price': origin_price, 'discount': discount, 'stock': stock}
            book_detail_dic = {'cover': cover, 'catalogue': catalogue, 'summary': summary}

            result = add_one_book(book_dic, book_detail_dic)
            if result:
                return render(request, 'manager/add_book_successfully.html', {'user': user})
            else:
                return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:  # 表单出错
            return render(request, 'manager/add_book_page.html', {'user': user, 'add_book_form': add_book_form})
    else:  # 当正常访问时
        add_book_form = AddBookForm
        return render(request, 'manager/add_book_page.html', {'user': user, 'add_book_form': add_book_form})


@user_passes_test(is_manager, login_url='manager:login')
def modify_book_page(request, book_id):
    user = auth.get_user(request)
    if request.method == 'POST':
        modify_book_form = ModifyBookForm(request.POST, request.FILES)
        if modify_book_form.is_valid():
            book_name = modify_book_form.cleaned_data.get('name')
            publisher = modify_book_form.cleaned_data.get('publisher')
            author = modify_book_form.cleaned_data.get('author')
            category = modify_book_form.cleaned_data.get('category')
            origin_price = modify_book_form.cleaned_data.get('origin_price')
            discount = modify_book_form.cleaned_data.get('discount')
            stock = modify_book_form.cleaned_data.get('stock')
            cover = modify_book_form.cleaned_data.get('cover')
            catalogue = modify_book_form.cleaned_data.get('catalogue')
            summary = modify_book_form.cleaned_data.get('summary')

            book_dic = {'name': book_name, 'publisher': publisher, 'author': author, 'category': category,
                        'origin_price': origin_price, 'discount': discount, 'stock': stock}
            book_detail_dic = {'cover': cover, 'catalogue': catalogue, 'summary': summary}

            result = modify_book(book_id, book_dic, book_detail_dic)
            if result:
                return render(request, 'manager/modify_book_successfully.html', {'user': user, 'book_id': book_id})
            else:
                return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:  # 表单出错
            return render(request, 'manager/modify_book_page.html',
                          {'user': user, 'modify_book_form': modify_book_form})
    else:  # 当正常访问时
        book = get_book_by_book_id(book_id)
        if book is None:
            return render(request, 'error.html', {'user': user, 'error_message': '出错啦'})
        else:
            modify_book_form = ModifyBookForm(
                {'book_id': book.book_id, 'name': book.name, 'publisher': book.publisher, 'author': book.author,
                 'category': book.category,
                 'origin_price': book.origin_price, 'discount': book.discount, 'stock': book.stock,
                 'cover': book.bookdetail.cover,
                 'catalogue': book.bookdetail.catalogue, 'summary': book.bookdetail.summary})
            return render(request, 'manager/modify_book_page.html',
                          {'user': user, 'modify_book_form': modify_book_form})


@user_passes_test(is_manager, login_url='manager:login')
def sold_out_or_putaway(request, book_id):
    redirect_to = request.GET.get('redirect_to')
    book = get_book_by_book_id(book_id)
    if book.is_on_sale:
        book.is_on_sale = False  # 下架
    else:
        book.is_on_sale = True  # 上架
    book.save()
    return redirect(redirect_to)


@user_passes_test(is_manager, login_url='manager:login')
def handle_orders(request):
    user = auth.get_user(request)
    page = request.GET.get('page', 1)
    orders = get_orders_by_user(user)
    contacts = get_books_to_page(orders, page=page)
    return render(request, 'user/look_orders_page.html', {'user': user, 'contacts': contacts})
