#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Vietronic'
__date__ = '$2017-2-17$'

import json
import requests
import re
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

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
        pa = r'\w\s\w{4}="/\w{3}/\w{3}\.\w{3}\?\w{3}=(.+?)&\w{4}=\d{3}&\w{5}=\d{3}&\w{4}=\w{5}"\w{5}="(.+?)"\s+\w{5}'

        res = re.findall(pa, self.page_text)
        # 如果和设定的值相同，表示没有更新
        if( res[0][0] == self.pointer):
            print('fuck')
            self.pointer = res[0][0]
            return

        msg_page_url = 'http://www.aao.cdut.edu.cn/aao/aao.php?aid=' + str(res[0][0]) + '&sort=389&sorid=391&from=passg'
        temp = requests.get( msg_page_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        })

        self.email_push( temp.text, res[0][1])
        return

    def email_push(self, msg_text, msg_header_text):
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        # 格式化信息
        msg = MIMEText(msg_text, 'html', 'utf-8')
        msg['From'] = _format_addr('Vietronic的自动推送邮件 <%s>' % self.config['address'])
        msg['Subject'] = Header( msg_header_text+'【自动推送】', 'utf-8').encode()

        # 连接服务器，使用SSL连接
        server = smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port'])
        server.set_debuglevel(0)

        # 登陆
        server.login(self.config['address'], self.config['password'])
        for i in self.config['email']:
            msg['To'] = _format_addr((i+' <%s>') % self.config['email'][i])
            # 发送邮件
            server.sendmail(self.config['address'], self.config['email'][i], msg.as_string())

        # 关闭连接
        server.quit()
        return

def main():
    check = auto_monitor()
    # 每半小时执行一次
    while True:
        check.text_filter()
        time.sleep(1800)
if __name__ == '__main__':
    main()




