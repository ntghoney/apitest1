# -*- coding: utf-8 -*-
'''
@File  : sendEmail.py
@Date  : 2019/1/15/015 17:32
'''
#gvbvpqbosvrybcic
import smtplib
from email.mime.text import MIMEText
from email.header import Header
sender = '740207942@qq.com'
receivers = ['2395027402@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("测试", 'utf-8')  # 发送者
message['To'] = Header("测试", 'utf-8')  # 接收者
print("1")
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

# try:
smtpObj = smtplib.SMTP("smtp.qq.com")
print(2)
smtpObj.login("740207942@qq.com","gvbvpqbosvrybcic")
smtpObj.sendmail(sender, receivers, message.as_string())

# except smtplib.SMTPException as e:
#     print(e)
#     print("发送失败")

