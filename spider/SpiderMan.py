# -*- coding: utf-8 -*-

from .DataOutput import DataOutput
from .HtmlDownloader import HtmlDownloader
from .HtmlParser import HtmlParser
from .URLManager import URLManager


class SpiderMan(object):
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url=None):
        if root_url is not None:
            # 添加入口url
            self.manager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓取了多少个url
        while (self.manager.has_new_url() and self.manager.old_url_size() < 3100):
            try:
                # 从URL管理器获取新的URL
                new_url = self.manager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                info, new_urls, datas = self.parser.parser(new_url, html)
                # 将抽取的URL添加到URL管理器中
                # self.manager.add_new_urls(new_urls)
                # 数据存储器存储数据
                self.output.output_data(datas, info['place'], info['title'])
                print
                info['place'], info['title']
                print
                '已经抓取%s个链接' % self.manager.old_url_size()
            except Exception as e:
                print(e)
                print('crawl failed')
        self.manager.save_progress('file/new_urls.txt', self.manager.new_urls)
        self.manager.save_progress('file/old_urls.txt', self.manager.old_urls)

    def crawl_page(self, root_page=None):
        self.manager.new_pages = self.manager.load_progress('file/new_pages.txt')  # 未爬取页面
        self.manager.old_pages = self.manager.load_progress('file/old_pages.txt')  # 已爬取页面
        if root_page is not None:
            # 添加入口url
            self.manager.add_new_page(root_page)
        while (self.manager.has_new_page() and self.manager.old_page_size() < 161):
            try:
                new_page = self.manager.get_new_page()
                html = self.downloader.download(new_page)
                new_pages, new_urls = self.parser.parser_page(new_page, html)
                self.manager.add_new_pages(new_pages)
                self.manager.add_new_urls(new_urls)
                print
                '已经抓取%s页' % self.manager.old_page_size()
            except Exception as e:
                print(e)
                print('crawl failed')
        self.manager.save_progress('file/new_urls.txt', self.manager.new_urls)
        self.manager.save_progress('file/new_pages.txt', self.manager.new_pages)
        self.manager.save_progress('file/old_pages.txt', self.manager.old_pages)

    def add_new_page(self, page_urls):
        self.manager.new_pages = self.manager.load_progress('file/new_pages.txt')  # 未爬取页面
        self.manager.old_pages = self.manager.load_progress('file/old_pages.txt')  # 已爬取页面
        self.manager.add_new_pages(set(page_urls))
        self.manager.save_progress('file/new_pages.txt', self.manager.new_pages)
        self.manager.save_progress('file/old_pages.txt', self.manager.old_pages)


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl_page()
    spider_man.crawl()

    # spider_man.add_new_page(['http://www.mm131.com/qingchun/','http://www.mm131.com/xinggan/','http://www.mm131.com/xiaohua/','http://www.mm131.com/chemo/','http://www.mm131.com/qipao/','http://www.mm131.com/mingxing/'])
