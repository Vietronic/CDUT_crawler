#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'
__date__ = '$2017-1-30$'

import requests
import re

PAGE_URL = 'http://www.aao.cdut.edu.cn/aao/aao.php?sort=389&sorid=391&from=more'

# 页面下载函数
def page_download(tempurl):
    return requests.get(tempurl, headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    })

# 正则表达式筛选页面
def text_filter(text):
    # 匹配模式
    pa = r'<a href="(.+?)"title="(.+?)"\s+class'
    res = re.findall(pa, text)
    str = ''
    for n, m in res:
        str += m + ' ' + 'http://www.aao.cdut.edu.cn' + n + '\n'
    # 找到下一页信息，如果存在则返回URL
    pa = r'<a href= (.+?)>下页</a>'
    res = re.findall(pa, text)
    if res:
        for n in res:
            tempurl = n
    else:
        tempurl = None
    return str, tempurl

# 写入文本
def file_process(text):
    # 使用UTF-8打开文件，以防出现编码错误
    file = open('./教务处公告.txt', 'w', encoding='utf-8')
    file.write(text)
    file.close()
    return

def main():
    url = PAGE_URL
    text = ''
    # 循环搜索并输出
    while url:
        res = page_download(url)
        temp_text, temp_url = text_filter(res.text)
        text += temp_text
        if temp_url:
            url = 'http://www.aao.cdut.edu.cn/aao/aao.php' + temp_url
        else:
            url = None
    file_process(text)

if __name__ == '__main__':
    main()