# -*- coding: utf-8 -*-
# date: 2023-6-20
"""
每隔5分钟检查一次ip，如果发生变化，发送邮件告知
"""
import smtplib
import subprocess
import time
from email.header import Header
from email.mime.text import MIMEText


def getip():
    p = subprocess.run('ipconfig', shell=True, stdout=subprocess.PIPE, encoding='gbk')
    return p.stdout


def sendmail(text):
    """
    发送邮件
    :param text: 邮件正文内容
    :return:
    """
    smtpObj = smtplib.SMTP('smtp.126.com', 25)  # smtp.xxx.com为邮箱服务类型，25为STMP
    # smtpObj = smtplib.SMTP_SSL('smtp.xxx.com', 'xxx邮件服务的端口号')
    smtpObj.login('wenliang1059@126.com', 'ZWMIFYREMOYMPTEG')  # 登录(账户，密码/授权码)
    message = MIMEText(text, 'plain', 'utf-8')  # text为邮件正文内容，plain为文本格式，'utf-8'为编码格式
    # message['From'] = Header(sender, 'utf-8')  # 发送者信息
    # message['To'] = Header(receiver, 'utf-8')  # 接收者消息
    message['Subject'] = Header('ip-' + time.ctime(), 'utf-8')  # 邮件主题
    smtpObj.sendmail('wenliang1059@126.com', ['wenliang1059@126.com', ], message.as_string())  # 发送(发件人，收件人列表，邮件信息)

    # 添加附件
    # message = MIMEMultipart()
    # message.attach(MIMEText('dear ,我发送一个附件给你清注意查收', 'plain', 'utf-8'))
    # # 邮件主题
    # subject = 'python测试附件'
    # message['Subject'] = subject
    # # 发送方信息
    # message['From'] = sender
    # # 接受方信息
    # message['To'] = receivers[0]
    #
    # att = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
    # att["Content-Type"] = 'application/octet-stream'
    #
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字,# 写中文乱了
    # att["Content-Disposition"] = 'attachment; filename="test.txt"'
    # message.attach(att)


if __name__ == '__main__':
    ip = ''
    while True:
        if (nextip := getip()) != ip:
            ip = nextip
            sendmail(ip)
        time.sleep(5 * 60)
