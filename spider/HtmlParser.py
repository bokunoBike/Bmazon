# -*- coding: utf-8 -*-

import re
import urlparse
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parser(self, page_url, html_cont):
        '''
        用于解析网页内容，抽取URL和数据
        :param page_url:下载页面的URL
        :param html_cont:下载的页面内容
        :return:返回URL和数据
        '''
        if page_url is None or html_cont is None:
            return
        # soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        soup = BeautifulSoup(html_cont, 'html.parser')
        main_info = self.get_main_info(page_url, soup)
        # new_urls=self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url, soup, main_info)
        # return main_info,new_urls,new_data
        return main_info, None, new_data

    def parser_page(self, page_url, html_cont):
        '''
        用于解析网页内容，抽取下一页url
        :param page_url:下载页面的URL
        :param html_cont:下载的页面内容
        :return:返回URL和数据
        '''
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_pages = self._get_next_page(page_url, soup)
        new_urls = self._get_page_urls(page_url, soup)
        return new_pages, new_urls

    def _get_next_page(self, page_url, soup):
        new_pages = set()
        link = soup.find('dd', class_='page').find('a', text=re.compile(u'下一页'))['href']
        new_full_link = urlparse.urljoin(page_url, link)
        new_pages.add(new_full_link)
        return new_pages

    def _get_page_urls(self, page_url, soup):
        '''
        抽取新的URL集合
        :param page_url:下载页面的URL
        :param soup:soup
        :return:返回新的URL集合
        '''
        new_urls = set()
        # 抽取符合要求的a标记
        links = soup.find('div', class_='main').find('dl').find_all('a', href=re.compile(
            r'(http://www.mm131.com/.*/\d+\.html)'))
        for link in links:
            # 提取href属性
            new_url = link['href']
            new_urls.add(new_url)
        place = soup.find('div', class_='main').find('dt', class_='public-title').find('a').find_next_sibling().text
        current_page = soup.find('dd', class_='page').find('span', class_='page_now').text
        print
        place, current_page
        return new_urls

    def _get_new_urls(self, page_url, soup):
        '''
        抽取新的URL集合
        :param page_url:下载页面的URL
        :param soup:soup
        :return:返回新的URL集合
        '''
        new_urls = set()
        # 抽取符合要求的a标记
        links = soup.find('div', class_='otherlist').find('ul').find_all('a', href=re.compile(r'(\d+\.html)'))
        for link in links:
            # 提取href属性
            new_url = link['href']
            # 拼接成完整网址
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup, main_info):
        '''
        抽取有效数据
        :param page_url:下载页面的URL
        :param soup:soup
        :return:返回有效数据
        '''
        title = main_info['title']
        total_page = main_info['total_page']
        url_image_id = main_info['url_image_id']
        datas = []
        for i in range(1, int(total_page) + 1):
            data = {}
            alt = title + '(%d)' % i
            data['alt'] = alt
            img_url = 'http://img1.mm131.com/pic/%s/%d.jpg' % (url_image_id, i)
            data['img_url'] = img_url
            datas.append(data)
        return datas

    def get_main_info(self, page_url, soup):
        main_info = {}
        title = soup.find('div', class_='content').find('h5').text
        place = soup.find('div', class_='place').find('a').find_next_sibling().text
        total_page_str = soup.find('div', class_='content-page').find('span').text
        total_page = re.findall(r'\d+', total_page_str)[0]
        url_image_id = \
            re.findall(r'http://img1.mm131.com/pic/(\d+)/1.jpg',
                       soup.find('div', class_='content-pic').find('img')['src'])[
                0]

        main_info['title'] = title
        main_info['place'] = place
        main_info['total_page'] = total_page
        main_info['url_image_id'] = url_image_id
        return main_info
