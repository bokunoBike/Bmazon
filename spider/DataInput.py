# -*- coding: utf-8 -*-
import os
import json
import pickle as cPickle
import requests
import random
import chardet
import shutil


class DataInput(object):
    def __init__(self):
        self.added_asins = self.load_progress('file/added_asins.txt')
        self.session = requests.session()
        postdata = {'username': 'bmazon', 'password': 'bmazon123456'}
        self.r = self.session.post('http://127.0.0.1:8000/manager/login', data=postdata)

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
        print('[+] 从文件加载进度： %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = cPickle.load(f)
                return tmp
        except:
            print('[!] 无进度文件，创建： %s' % path)
        return set()

    def add_added_asin(self, asin):
        if asin is None:
            return
        if asin not in self.added_asins:
            os.chdir('books')
            shutil.rmtree(asin)
            os.chdir('..')
        self.added_asins.add(asin)

    def get_book_info(self, asin):
        os.chdir('books')
        os.chdir(asin)
        with open('book_info.txt', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['name'] = data.get('title')
        data['origin_price'] = data.get('price')
        author = ''
        for i in data.get('authors'):
            author += (i + ',')
        author = author[:-1]
        data['author'] = author
        data['stock'] = random.randint(5, 100)
        data['discount'] = random.randint(13, 20) * 5 / 100
        files = {}
        files['cover'] = open('cover.jpg', 'rb')
        files['catalogue'] = open('catalogue.txt', 'rb')
        files['summary'] = open('summary.txt', 'rb')
        os.chdir('..')
        os.chdir('..')
        return data, files

    def add_book_info(self, asin):
        data, files = self.get_book_info(asin)
        r = self.session.post('http://127.0.0.1:8000/manager/add_book_page', data=data, files=files)
        print('add ' + data['title'])

    def add_book(self):
        os.chdir('books')
        asins = os.listdir()
        os.chdir('..')
        for asin in asins:
            self.add_book_info(asin)
            self.add_added_asin(asin)
            self.save_progress('file/added_asins.txt', self.added_asins)

if __name__ == '__main__':
    datainput = DataInput()
    datainput.add_book()
