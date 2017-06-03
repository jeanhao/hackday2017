# -*- coding: utf-8 -*-

from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


HOST = 'smtp.exmail.qq.com'
SUBJECT = u'步灵科技用户反馈'
# FROM = "schoolblackmarket@163.com"
FROM = "info@brainagi.com"
PASSWORD = 'Bulingkeji2017'

def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    mail_coding = 'utf-8'
    att_header = Header(os.path.basename(src), mail_coding);
    msgImage.add_header('Content-Disposition', 'attachment; filename="%s"' % att_header)
#     msgImage.add_header('Content-ID', imgid)
    return msgImage

def send_mail(to=FROM, text="用户信息反馈邮件", imgsrc=None):
    msg = MIMEMultipart('related')
    msgtext = MIMEText(text, "html", "utf-8")
    msg.attach(msgtext)
    if imgsrc:
        msg.attach(addimg(imgsrc, "weekly"))

    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = to
    try:
        server = smtplib.SMTP()
        server.connect(HOST)
        server.login(FROM, PASSWORD)
        server.sendmail(FROM, to, msg.as_string())
        server.quit()
        print "邮件发送成功！"
    except Exception, e:
        print "失败：" + str(e)

if __name__ == '__main__':
    send_mail(FROM)

