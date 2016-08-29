# coding=utf8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT

server = MAIL_SERVER
port = MAIL_PORT
from_addr = MAIL_USERNAME
password = MAIL_PASSWORD

def sendEmail(subject, content, type, emailAdd):
    message = MIMEText(content, type, 'utf-8')
    message['From'] = Header("周于涛", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(server, 465)
        smtpObj.set_debuglevel(1)
        smtpObj.login(from_addr, password)
        smtpObj.sendmail(from_addr, [emailAdd], message.as_string())
        smtpObj.quit()
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print "Error: 无法发送邮件", e