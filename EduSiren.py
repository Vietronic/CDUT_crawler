#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Vietronic'
__date__ = '$2017-4-11$'

# 导呀导呀我的骄傲放纵
import json
import requests
import re
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from lxml import etree



class CdutEduSiren:
    __name__ = 'EduSiren'

    def __init__(self):
        # 加载config配置文件
        def load_config():
            f = open('./config.json', 'r', encoding='utf-8')
            config = json.load(f)
            f.close()
            print('The configuration file has been loaded correctly.'.encode("gb2312"))
            return config
        # 初始化配置信息
        self.config = load_config()
        self.url = self.config['PAGE_URL']
        self.pointer = self.config['pointer']
        self.page_text = ''

    # 页面下载函数
    def page_download(self):
        # 错误处理机制防止获取页面出错
        try:
            temp = requests.get(
                self.url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            )
            # 如果响应状态码不是 200，就主动抛出异常
            temp.raise_for_status()
        except requests.RequestException as e:
            print(e)
        else:
            # 执行此函数便更新类中的文本变量
            self.page_text = temp.text
        return

    #
    def filter_process(self):
        # 下载页面，刷新页面文本值
        self.page_download()

        textTree = etree.HTML(self.page_text)

        # 获取最新消息链接
        node = textTree.xpath('//*[@id="news_content"]/table/tr[2]/td/table/tr[1]/td/a/@href')

        if(node is not None):
            # 匹配模式
            pa = r'\w{3}\.\w{3}\?\w{3}=(.+?)&\w{4}=\d*&\w{5}=\d*&\w{4}=\w{5}'
            # 搜索内容
            res = re.findall(pa, node[0])
            PointerNum = res[0]

            # 获取消息标题
            PointerTitle = textTree.xpath('//*[@id="news_content"]/table/tr[2]/td/table/tr[1]/td/a/@title')[0]

            # 判断是否为初次启动
            if ( self.pointer == '0'):
                # 发送启动服务通知邮件
                start_text = '您的自动推送服务已启动。'
                title_text = '服务启动通知'
                self.email_push( start_text, title_text)
                print('The siren service is ready. ' + 'Time: ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                self.pointer = PointerNum
                return

            # 如果和设定的值相同，表示没有更新
            if (PointerNum == self.pointer):
                print('No new file. Num: ' + self.pointer + 'Time: ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                return

            # 若有新内容，则下载该页面并发送
            msg_page_url = 'http://www.aao.cdut.edu.cn/aao/aao.php?aid=' + str(PointerNum) + '&sort=389&sorid=391&from=passg'
            try:
                temp = requests.get(msg_page_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
                })

                # 发送邮件
                self.email_push(temp.text, PointerTitle)

                # 发送邮件后重设指标值
                self.pointer = PointerNum
            except requests.RequestException as e:
                print(e)
        return

    # 邮件发送函数
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
        print('Message has been sent, Num: ' + self.pointer + ' Time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return

def main():
    check = CdutEduSiren()
    # 循环保持运行，每半小时执行一次
    while True:
        check.filter_process()
        time.sleep(1800)

if __name__ == '__main__':
    main()




