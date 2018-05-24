# -*- coding: utf-8 -*-

import urllib.request
import os
import json
import shutil


class DataOutput(object):
    def output_data(self, datas, asin):
        os.chdir('books')
        if not os.path.exists(asin):
            os.makedirs(asin)
            os.chdir(asin)
            try:
                with open('catalogue.txt', 'w', encoding='utf-8') as f:
                    f.write(datas.get('catalogue'))
                    datas.pop('catalogue')
                    f.close()  # 关闭文件
                with open('summary.txt', 'w', encoding='utf-8') as f:
                    f.write(datas.get('summary'))
                    datas.pop('summary')
                    f.close()  # 关闭文件
                cover_src = datas.get('cover_src')
                datas.pop('cover_src')
                with open('book_info.txt', 'w', encoding='utf-8') as f:
                    json.dump(datas, f)
                    f.close()  # 关闭文件
                urllib.request.urlretrieve(cover_src, 'cover.jpg')
                print('' + asin + ' finish')
                os.chdir('..')
            except Exception as e:
                print(e)
                os.chdir('..')
                shutil.rmtree(asin)
            finally:
                os.chdir('..')
        else:
            print('已经存在')
            os.chdir('..')
        return
