# -*- coding: utf-8 -*-
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from urllib import parse

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
url = 'https://www.amazon.cn/s?ie=UTF8&page=2&rh=n%3A658876051'
url = 'https://www.amazon.cn/s?ie=UTF8&page=1&rh=n%3A658876051'
r = requests.get(url)
soup = BeautifulSoup(str(r.content, 'utf-8').replace('\n', ''), 'html.parser')
page_bar = soup.find('div',
                     class_="a-fixed-left-flipped-grid s-padding-left-small s-padding-right-small s-span-page a-spacing-top-small")

next_page = soup.find('a', class_="pagnNext", id="pagnNextLink", title="下一页")
new_full_link = parse.urljoin(url, next_page['href'])

print(new_full_link)
atfResults = soup.find('div', id=["atfResults", "mainResults"], class_="a-row s-result-list-parent-container")
print(atfResults)
lis = atfResults.find('ul').find_all(
    'li', class_="s-result-item celwidget ")
for li in lis:
    # 提取href属性
    new_url = li['data-asin']
    print(new_url)
