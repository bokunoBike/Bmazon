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
            r.encoding = chardet.detect(r.content)['encoding']
            return r.text
        return None

htmld = HtmlDownloader()
print(htmld.download(url='https://www.amazon.cn/gp/product/B0788XVV8D/ref=s9_acsd_al_bw_c_x_2_w?pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-2&pf_rd_r=XH09SVWVPG58ARGZ1ZMM&pf_rd_r=XH09SVWVPG58ARGZ1ZMM&pf_rd_t=101&pf_rd_p=69cd0f53-b0a8-4915-bd08-3c4e010da701&pf_rd_p=69cd0f53-b0a8-4915-bd08-3c4e010da701&pf_rd_i=116099071'))
