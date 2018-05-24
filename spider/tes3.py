# -*- coding: utf-8 -*-
import requests
import urllib.request
import re
from bs4 import BeautifulSoup
import json

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

asin = 'B078FFX8B6'
asin = 'B00MN73ETM'
r1 = requests.post(
    'https://www.amazon.cn/gp/product-description/ajaxGetProuductDescription.html?ref_=dp_apl_pc_loaddesc&asin=%s&deviceType=web' % (
        asin), headers=headers)
soup = BeautifulSoup(str(r1.content, 'utf-8').replace('\n', ''), 'html.parser')
catalogue = soup.find('div', id="s_contents", class_="s-contents").find('h3', text="目录").next_sibling.next_sibling
catalogue = str(catalogue).replace('<p>', '\n').replace('</p>', '\n').replace('<br/>', '\n').strip()

summary = soup.find('div', id="s_contents", class_="s-contents").find('h3', text="文摘").next_sibling.next_sibling
summary = str(summary).replace('<p>', '\n').replace('</p>', '\n').replace('<br/>', '\n').strip()

postdata = {'asin': asin, 'method': 'getBookData'}
r2 = requests.post('https://www.amazon.cn/gp/search-inside/service-data', data=postdata)
data = json.loads(str(r2.content, 'utf-8').strip())
title = data.get('title')
price = data.get('buyingPrice')
authors = data.get('authorNameList')
print(data)
cover_src = data.get('largeImageUrls')
if cover_src is not None:
    cover_src = cover_src['1']
else:
    cover_src = data.get('thumbnailImage').replace('._SL75_', '')

r3 = requests.get('https://www.amazon.cn/dp/%s' % asin, headers=headers)
soup = BeautifulSoup(str(r3.content, 'utf-8').replace('\n', ''), 'html.parser')
publisher = soup.find('div', id="detail_bullets_id").find('div', class_="content").ul.find('b', text=re.compile(
    r'出版社')).next_sibling
categorys = soup.find('div', id="wayfinding-breadcrumbs_container",
                      class_="a-section a-spacing-none a-padding-medium").find('ul',
                                                                               class_="a-unordered-list a-horizontal a-size-small").find_all(
    'a', class_="a-link-normal a-color-tertiary")
if len(categorys) > 1:
    category = categorys[1].text.strip()
else:
    category = categorys[0].text.strip()

book_info = {'title': title, 'authors': authors, 'price': price, 'publisher': publisher, 'category': category,
             'cover_src': cover_src, 'catalogue': catalogue, 'summary': summary}
print(book_info)
