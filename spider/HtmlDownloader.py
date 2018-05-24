# -*- coding: utf-8 -*-
'''
Created on 2017年8月6日

@author: user
'''

import requests
import chardet


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User_Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            # r.encoding = chardet.detect(r.content)['encoding']
            # print(r.text)
            return r.text
        return None
