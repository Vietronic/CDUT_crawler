#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'

import requests
import hashlib
import re
import xlrd
import xlwt
# import time

# POST地址
LOGIN_URL = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'
INFO_URL = 'http://202.115.133.173:805/Default.aspx'
SCORE_URL = 'http://202.115.133.173:805/SearchInfo/Score/ScoreList.aspx'
# 浏览器标志头
CHROME_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
# 抓取的总信息数量
ROW_NUM = 10

class stu:
    def __init__(self, stuNum, pwd):
        # 计算MD5处理后的密码
        def getPwd(userName, userPwd, signTime):
            a = hashlib.md5(userPwd.encode())
            b = userName + signTime + a.hexdigest()
            temp = hashlib.md5(b.encode())
            return temp.hexdigest()
        # POST字典
        self.postData = {'Action': 'Login', 'userName': stuNum, 'pwd': getPwd(stuNum, pwd, str(1)), 'sign': '1'}
        # 学生信息
        self.info = {'num': stuNum}
        # 简化代码，优化效率
        # # 时间戳
        # self.signTime = int(time.time()*1000)
        # # 登陆密码
        # self.signedPwd = getPwd(stuNum, pwd, str(self.signTime))
        # # POST字典
        # self.postData = { 'Action': 'Login', 'userName': stuNum, 'pwd': self.signedPwd, 'sign': self.signTime}

    def setInfo(self):
        # 创建一个会话
        ses = requests.session()
        # 通过POST方法登陆
        temp = ses.post(LOGIN_URL, data=self.postData, headers=CHROME_HEADERS)
        # 获取学生信息页面
        info = ses.get(INFO_URL, headers=CHROME_HEADERS).text

        # 通过正则表达式抓取学生信息
        pa = r'姓名：(.+?)</li>'
        res = re.findall(pa, info)
        self.info['name'] = res[0]

        pa = r'<li>院系：(.+?)</li>'
        res = re.findall(pa, info)
        self.info['col'] = res[0]

        pa = r'<li>专业：(.+?)</li>'
        res = re.findall(pa, info)
        self.info['major'] = res[0]

        # print(self.info)
        return

    def getPage(self):
        # 创建一个会话
        ses = requests.session()
        # 通过POST方法登陆
        temp = ses.post( LOGIN_URL, data=self.postData, headers=CHROME_HEADERS)
        # 获取成绩页面
        scoreTemp = ses.get( SCORE_URL, headers=CHROME_HEADERS)

        # 使用UTF-8打开文件，以防出现编码错误
        file = open('./成绩信息.txt', 'w', encoding='utf-8')
        file.write(scoreTemp.text)
        file.close()
        return

    def getScore(self):
        file = open('./成绩信息.txt', 'r', encoding='utf-8')  # 使用UTF-8打开文件，以防出现编码错误
        s = file.read()
        file.close()

        file = open('./成绩.txt', 'w', encoding='utf-8')
        pa = r'<\w{3}\s\w{5}="\w{8}\d0"\s\w{5}="\w{5}:\s\d+%;">\s+(.+?)&\w{4};\s+</\w{3}>'
        res = re.findall(pa, s)
        l = len(res)
        i = 0
        while (i != l):
            temp = res[i:(i + 10)]
            for n in temp:
                file.write(n+' ')
            file.write('\n')
            i += 10
        file.close()
        return

def main():
    book = xlrd.open_workbook('test.xls')
    # 创建 xls 文件对象
    wb = xlwt.Workbook()
    # 新增一个表单
    sheet_write = wb.add_sheet('info')

    sh = book.sheet_by_index(0)
    row = 1
    while (row <= ROW_NUM):
        stuNum = sh.cell_value(row, 0)
        id = sh.cell_value(row, 1)
        name = sh.cell_value(row, 2)
        # 创建学生对象，分别填入学号和密码，均为字符串输入
        temp = stu(stuNum, id)
        temp.setInfo()

        # 按位置添加数据
        sheet_write.write(row - 1, 0, stuNum)
        sheet_write.write(row - 1, 1, id)
        sheet_write.write(row - 1, 2, name)
        sheet_write.write(row - 1, 3, temp.info['name'])
        sheet_write.write(row - 1, 4, temp.info['major'])
        sheet_write.write(row - 1, 5, temp.info['col'])
        del temp
        row += 1
        if(row%700==0):
            print('完成了',row/ROW_NUM,'%')

    # 保存文件
    wb.save('example.xls')

if __name__ == '__main__':
    main()