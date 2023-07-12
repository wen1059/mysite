# -*- coding: utf-8 -*-
# date: 2023-6-20
"""
每隔5分钟检查一次ip，如果发生变化，发送邮件告知
"""
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time


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


if __name__ == '__main__':
    ip = ''
    while True:
        if (nextip := getip()) != ip:
            ip = nextip
            sendmail(ip)
        time.sleep(5 * 60)
