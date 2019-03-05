# -*- coding: utf-8 -*-

from spider.DataOutput import DataOutput
from spider.HtmlDownloader import HtmlDownloader
from spider.HtmlParser import HtmlParser
from spider.URLManager import URLManager
import copy


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
        while self.manager.has_new_url() and self.manager.old_url_size() < 400:
            try:
                # 从URL管理器获取新的URL
                new_asin = self.manager.get_new_url()
                # new_url = 'https://www.amazon.cn/dp/' + new_asin
                # HTML下载器下载网页
                # HTML解析器抽取网页数据
                datas = self.parser.parser(new_asin)
                # 数据存储器存储数据
                self.output.output_data(datas, new_asin)
                self.manager.save_progress('file/new_urls.txt', self.manager.new_urls)
                self.manager.save_progress('file/old_urls.txt', self.manager.old_urls)
                print('已经抓取%s个链接，剩余%s个链接' % (self.manager.old_url_size(), self.manager.new_url_size()))
            except Exception as e:
                self.manager.add_error_asin(new_asin)
                print(e)
                print('crawl failed ' + new_asin)
                self.manager.save_progress('file/error_asins.txt', self.manager.error_asins)

    def crawl_error(self, root_url=None):
        if root_url is not None:
            # 添加入口url
            self.manager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓取了多少个url
        icount = 0
        error_asins2 = copy.deepcopy(self.manager.error_asins)
        for error_asin in error_asins2:
            if self.manager.old_url_size() < 400:
                try:
                    # HTML解析器抽取网页数据
                    datas = self.parser.parser(error_asin)
                    # 数据存储器存储数据
                    self.output.output_data(datas, error_asin)
                    self.manager.error_asins.remove(error_asin)
                    self.manager.old_urls.add(error_asin)
                    self.manager.save_progress('file/error_asins.txt', self.manager.error_asins)
                    self.manager.save_progress('file/old_urls.txt', self.manager.old_urls)
                    print('已经抓取%s个链接' % self.manager.old_url_size())
                except Exception as e:
                    print(e)
                    print('crawl failed ' +error_asin)
                    self.manager.save_progress('file/error_asins.txt', self.manager.error_asins)
                finally:
                    icount += 1
                    if icount >= 500:
                        break

    def crawl_page(self, root_page=None):
        self.manager.new_pages = self.manager.load_progress('file/new_pages.txt')  # 未爬取页面
        self.manager.old_pages = self.manager.load_progress('file/old_pages.txt')  # 已爬取页面
        if root_page is not None:
            # 添加入口url
            self.manager.add_new_page(root_page)
        while self.manager.has_new_page() and self.manager.old_page_size() < 70:    # 表示总共要抓取的页面数
            new_page = self.manager.get_new_page()
            html = self.downloader.download(new_page)
            new_pages, new_urls = self.parser.parser_page(new_page, html)
            self.manager.add_new_pages(new_pages)
            self.manager.add_new_urls(new_urls)
            print('已经抓取%s页' % self.manager.old_page_size())
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
    spider_man.crawl_page('https://www.amazon.cn/s/ref=amb_link_12?ie=UTF8&page=1&rh=n%3A658579051&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-leftnav&pf_rd_r=M7MMKEFSMVCBY4WY0CD6&pf_rd_r=M7MMKEFSMVCBY4WY0CD6&pf_rd_t=101&pf_rd_p=010f8d75-7563-4f80-a4bc-dfe74d89af9a&pf_rd_p=010f8d75-7563-4f80-a4bc-dfe74d89af9a&pf_rd_i=2133034051')
    spider_man.crawl()
    # spider_man.crawl_error()
