# -*- coding: utf-8 -*-

import cPickle
import hashlib


class URLManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('file/new_urls.txt')  # 未爬取URL集合
        self.old_urls = self.load_progress('file/old_urls.txt')  # 已爬取URL集合
        self.new_pages = None
        self.old_pages = None

    def has_new_page(self):
        """
        判断是否有未爬取的page
        :return:
        """
        return self.new_page_size() != 0

    def get_new_page(self):
        """
        获取一个未爬取的page
        :return:
        """
        new_page = self.new_pages.pop()
        m = hashlib.md5()
        m.update(new_page)
        self.old_pages.add(m.hexdigest()[8:-8])
        return new_page

    def add_new_page(self, page):
        """
        将新的page添加到未爬取的page集合中
        :param page:单个page
        :return:
        """
        if page is None:
            return
        m = hashlib.md5()
        m.update(page)
        page_md5 = m.hexdigest()[8:-8]
        if page not in self.new_pages and page_md5 not in self.old_pages:
            self.new_pages.add(page)

    def add_new_pages(self, pages):
        """
        将新的page添加到未爬取的page集合中
        :param page:page集合
        :return:
        """
        if pages is None or len(pages) == 0:
            return
        for page in pages:
            self.add_new_page(page)

    def new_page_size(self):
        """
        获取未爬取page集合的大小
        :return:
        """
        return len(self.new_pages)

    def old_page_size(self):
        """
        获取已爬取page集合的大小
        :return:
        """
        return len(self.old_pages)

    def has_new_url(self):
        """
        判断是否有未爬取的URL
        :return:
        """
        return self.new_url_size() != 0

    def get_new_url(self):
        """
        获取一个未爬取的URL
        :return:
        """
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self, url):
        """
        将新的URL添加到未爬取的URL集合中
        :param url:单个URL
        :return:
        """
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """
        将新的URL添加到未爬取的URL集合中
        :param url:URL集合
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        """
        获取未爬取URL集合的大小
        :return:
        """
        return len(self.new_urls)

    def old_url_size(self):
        """
        获取已爬取URL集合的大小
        :return:
        """
        return len(self.old_urls)

    def save_progress(self, path, data):
        '''
        保存进度
        :param path:文件路径
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            cPickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        '''
        print
        '[+] 从文件加载进度： %s' % path
        try:
            with open(path, 'rb') as f:
                tmp = cPickle.load(f)
                return tmp
        except:
            print
            '[!] 无进度文件，创建： %s' % path
        return set()