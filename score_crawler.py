#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'

import requests
import time
import hashlib

class CDUT:
    def __init__(self, name, pwd):
        # 计算MD5处理后的密码
        def getPwd(userName, userPwd, signTime):
            temp = hashlib.md5()
            temp.update(str(userPwd).encode())
            temp_str = str(userName) + str(signTime) + str(temp.hexdigest())
            temp.update(temp_str.encode())
            return temp.hexdigest()
        # POST地址
        self.loginUrl = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'
        # 时间戳
        self.signTime = int(time.time())
        # 密码
        self.signedPwd = getPwd(name, pwd, self.signTime)
        # POST字典
        self.postData = { 'Action': 'Login', 'userName': name, 'pwd': self.signedPwd, 'sign': self.signTime}
        print(self.postData)

    def getPage(self):
        ses = requests.session()
        temp = ses.post( self.loginUrl, json=self.postData, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        })
        cooker = temp.cookies.get_dict()
        print(temp.text)
        print(cooker)

        # temp2 = requests.get( 'http://202.115.133.173:805/Default.aspx', cookies=cooker, headers={
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        # })
        # temp2.encoding = 'utf-8'
        # print(temp2.text)

        return

def main():
    # 分别填入学号和密码
    a = CDUT( '', '')
    a.getPage()

if __name__ == '__main__':
    main()