#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Vietronic'
__date__ = '$2017-2-17$'

import json
import requests
import re

class auto_monitor:
    def __init__(self):
        def load_config():
            f = open('./config.json', 'r', encoding='utf-8')
            config = json.load(f)
            f.close()
            return config
        self.config = load_config()
        self.url = self.config['PAGE_URL']
        self.pointer = self.config['pointer']
        self.page_text = ''


    # 页面下载函数
    def page_download(self):
        temp = requests.get(self.url, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        })
        self.page_text = temp.text
        return

    # 正则表达式筛选页面
    def text_filter(self):
        # 下载页面，刷新页面文本值
        self.page_download()

        # 匹配模式
        pa = r'\w\s\w{4}="/\w{3}/\w{3}\.\w{3}\?\w{3}=(.+?)&\w{4}=\d{3}&\w{5}=\d{3}&\w{4}=\w{5}"\w{5}=".+?"\s+\w{5}'
        res = re.findall(pa, self.page_text)
        print(res[0])
        # 如果和设定的值相同，表示没有更新
        if( res[0] == self.pointer):
            print('fuck')
            self.pointer = res[0]
            return
        # str = ''
        # temp = res[0][0]
        # str = 'http://www.aao.cdut.edu.cn/aao/aao.php?aid=' + temp +'&sort=389&sorid=391&from=passg'
        # print(temp, str)
        return

    def email(self):
        print(['email'])
        return

def main():
    check = auto_monitor()
    check.text_filter()

if __name__ == '__main__':
    main()




