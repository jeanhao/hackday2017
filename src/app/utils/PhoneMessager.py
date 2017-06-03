#!/usr/bin/env python
# coding=utf8

'''
Step 1. 获取主题引用
'''
# 从https://account.console.aliyun.com/#/secure获取$YourAccountid
# 从https://ak-console.aliyun.com/#/accesskey获取$YourAccessId和$YourAccessKey
# 从http://$YourAccountId.mns.cn-hangzhou.aliyuncs.com获取$YourMNSEndpoint, eg. http://1234567890123456.mns.cn-hangzhou.aliyuncs.com
from app.utils.mns.account import Account
from app.utils.mns.topic import DirectSMSInfo, TopicMessage
from app.utils.mns.mns_exception import MNSExceptionBase
from app.utils.MyLogger import GFLogger


AccessKeyId = "RSql3v1W1UKHfNsV"
AccessKeySecret = "tIhgbvUhywT4anYNqBE5wUkQ0HhOOR"
Endpoint = "http://1003030461973760.mns.cn-hangzhou.aliyuncs.com/"
topicName = "sms.topic-cn-hangzhou"
my_account = Account(Endpoint, AccessKeyId, AccessKeySecret)
my_topic = my_account.get_topic(topicName)
free_sign_name = "植物说"
template_code = "SMS_69970152"
msg_body = "植物说消息"

def send_message(receiver, code, name="用户"):
    # 设置SMSSignName和SMSTempateCode
    direct_sms_attr = DirectSMSInfo(free_sign_name=free_sign_name, template_code=template_code, single=False)
    # 指定接收短信的手机号并指定发送给该接收人的短信中的参数值（在短信模板中定义的）
    direct_sms_attr.add_receiver(receiver=receiver, params={"name": name, "code":code})

    msg = TopicMessage(msg_body, direct_sms=direct_sms_attr)

    try:
        # 发布SMS消息
        my_topic.publish_message(msg)
        return True
    except MNSExceptionBase, e:
        if e.type == "TopicNotExist":
            GFLogger.error("Topic not exist, please create it.")
        return False

if __name__ == '__main__':
    send_message("15629071220", "曾豪", "12345")
