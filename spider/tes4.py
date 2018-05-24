# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {
    'Host': 'www.amazon.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Content-Length': '0',
}
s = requests.session()
postdata = {'username': 'bmazon', 'password': 'bmazon123456'}
r = s.post('http://127.0.0.1:8000/manager/login', data=postdata)
print(r.content)
r = s.get('http://127.0.0.1:8000/manager/add_book_page')
print(r.content)
