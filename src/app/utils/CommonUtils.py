# coding=UTF-8

import json, random, string, urllib, urllib2
import time, traceback
import xml.etree.ElementTree as ET
from app.utils.MyLogger import MyLoggerFactory
from app.utils.RetDefine import RetDefine
import datetime


fmtsp = '%Y-%m-%d'
fmtdl = '%Y-%m-%d %H:%M:%S'
logger = MyLoggerFactory().getLogger(__name__)

def pack(ret_status=RetDefine.NO_ERR, data=None):
    ret = {'status':ret_status}
    if data:
        ret['data'] = data
    return json.dumps(ret)

def unpack(text):
    if text:
        try:
            data = json.loads(text)
            return data
        except ValueError:
            logger.error(traceback.format_exc())
    return None

def filterMap(data, keys):
    return {key:data[key] for key in keys if key in data}

def send_req(url, data=None):
        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url=url)
        ret = urllib2.urlopen(request)
        return ret.read()

def gen_ramdon_string(length=10):
    return string.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], length)).replace(' ', '')

def get_now_date():
    return str(int((time.time() * 1000)))

def get_now_time(offset=0, detail=False):
    now = datetime.datetime.now()
    if offset:
        days = datetime.timedelta(days=offset)
        now = now - days
    fmt = fmtdl if detail else fmtsp
    return  now.strftime(fmt)

def xml2dict(text):
    root = ET.fromstring(text)
    for each in root.getiterator("xml"):
        data = each.attrib
        for childNode in each.getchildren():
            data[childNode.tag] = childNode.text
        return data