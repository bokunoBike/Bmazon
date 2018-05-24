# -*- coding: utf-8 -*-
from spider.HtmlDownloader import HtmlDownloader
from bs4 import BeautifulSoup
import urllib.request
import re

downloader = HtmlDownloader()
root_url = 'https://www.amazon.cn/dp/B06XPVL26Y'
html_cont = downloader.download(root_url)
# print(html_cont)

soup = BeautifulSoup(html_cont, 'html.parser')

# mainResults = soup.find('div', id="mainResults", class_="a-row s-result-list-parent-container")
# lis = mainResults.find('ul', class_="s-result-list s-col-1 s-col-ws-1 s-result-list-hgrid s-height-equalized s-list-view s-text-condensed").find_all('li', class_="s-result-item celwidget ")
# page_bar = soup.find('div', class_="a-fixed-left-flipped-grid s-padding-left-small s-padding-right-small s-span-page a-spacing-top-small")
# next_page = soup.find('a', class_="pagnNext", id="pagnNextLink", title="下一页")
# # for li in lis:
# #     print(li['data-asin'])
# print(next_page['href'])

# centerCol = soup.find('div', id="a-page").find('div', id="dp-container", class_="a-container").find('div', id="centerCol", class_="centerColumn")
# print(centerCol)
# title = centerCol.find('span', id="productTitle", class_="a-size-large").text
# authors = []
# authors_node = centerCol.find('div', id="bylineInfo", class_="a-section a-spacing-micro bylineHidden feature").find_all('span', class_="author")
# for author_node in authors_node:
#     authors.append(author_node.a.text)
# price = centerCol.find('div', id="MediaMatrix", class_="feature").find('ul', class_="a-unordered-list a-nostyle a-button-list a-horizontal").find('li', class_="swatchElement selected").find('span', class_="a-button-inner").find('span', class_="a-size-base a-color-price a-color-price").text.strip()[1:]
publisher = soup.find('div', id="detail_bullets_id").find('div', class_="content").ul.find('b', text=re.compile(r'出版社')).next_sibling
categorys = soup.find('div', id="wayfinding-breadcrumbs_container", class_="a-section a-spacing-none a-padding-medium").find('ul', class_="a-unordered-list a-horizontal a-size-small").find_all('a', class_="a-link-normal a-color-tertiary")
catalogue = soup.find('div', id="descriptionAndDetails", class_="a-section a-spacing-extra-large")
# cover_src = soup.find('div', id="dp-container", class_="a-container").find('div', id="leftCol").find('img', id="imgBlkFront", class_="a-dynamic-image image-stretch-vertical frontImage")['src']
# urllib.request.urlretrieve(cover_src, 'cover.jpg')
if len(categorys) > 1:
    category = categorys[1].text.strip()
else:
    category = categorys[0].text.strip()
# print(title)
# print(authors)
# print(price)
print(publisher)
print(category)
print(catalogue)
# print(cover_src)
