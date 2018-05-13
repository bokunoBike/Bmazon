# -*- coding: utf-8 -*-

import urllib
import os


class DataOutput(object):
    def output_data(self,datas,place,title):
        os.chdir('image')
        if not os.path.exists(place):
            os.makedirs(place)
        if not os.path.exists('%s/%s'%(place,title)):
            os.chdir(place)
            os.makedirs(title)
            os.chdir('..')
        else:
            print('已经存在')
            return
        os.chdir(place)
        os.chdir(title)
        for data in datas:
            urllib.urlretrieve(data['img_url'],'%s.jpg'%data['alt'])
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')