#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年4月30日

@author: zenghao
'''
from app.utils.CommonUtils import md5, send_req, send_json
from app.utils.mp.MpManager import MpManager
from app.utils.FileUploader import MultipartPostHandler
import cookielib
import urllib2
from app.utils.Singleton import singleton

@singleton
class CustomeServiceManager(object):
    '''
    @note: 克服相关管理
    '''

    def __init__(self):
        self.mpManager = MpManager()
        self.CUSTOMSERVICE_ADD_URL = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s"
        self.CUSTOMSERVICE_DEL_URL = "https://api.weixin.qq.com/customservice/kfaccount/del?access_token=%s"
        self.UPLOAD_IMG_URL = "http://api.weixin.qq.com/customservice/kfaccount/uploadheadimg?access_token=%s&kf_account=%s"
        self.KF_LIST = "https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s"

    def addOrdelCs(self, kf_account, nickname, password, oper="add", token=None):
        if not token:
            token = self.mpManager.getToken()
        data = {
            "kf_account" : kf_account,
            "nickname" : nickname,
            "password" : md5(password)
        }
        url = (self.CUSTOMSERVICE_ADD_URL if oper == 'add' else self.CUSTOMSERVICE_DEL_URL) % token
        res = send_req(url, data)
        return res

    def uploadimg(self, file, kf_account, token=None):
        url = self.UPLOAD_IMG_URL % (token if token else self.mpManager.getToken(), kf_account)
        params = {
            "file":file
        }
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                      MultipartPostHandler)
        res = opener.open(url, params).read()
        return res

    def getkflist(self, token=None):
        token = token if token else self.mpManager.getToken()
        res = send_req(self.KF_LIST % token)
        return res

if __name__ == '__main__':
#     print CustomeServiceManager().addOrdelCs("xiaosan@XYL125511", "小三", "qwe123")
#     print CustomeServiceManager().getkflist()
    print CustomeServiceManager().sendMsg("o-UJCxIpgmE8Mq_KaYaJXdoOsWWw", "text", {"content":"测试实施适度hi上帝"})

