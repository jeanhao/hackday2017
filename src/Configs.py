# -*- coding: utf-8 -*-
METHODS = ['POST', 'GET']  # 统一方法请求类型
POST = ['POST']
GET = ['GET']

######### DBConfig begin  ##########

class dbOper:
    READ = 1
    WRITE = 2
    ALL = 3

dbConfigs = []

DEFAULT_DB_NAME = 'default'
DEFAULT_DB_RATE = 100
DEFAULT_DB_HOST = 'localhost'
DEFAULT_DB_PORT = 3306
DEFAULT_DB_NAME = 'hackday_plant'
DEFAULT_DB_USER = 'root'
DEFAULT_DB_PASSWD = 'Hustonline87542701'
DEFAULT_DB_CHARSET = 'utf8mb4'
DEFAULT_DB_MINCACHED = 1
DEFAULT_DB_MAXCACHED = 20

def db_config_maker(name=DEFAULT_DB_NAME, rate=DEFAULT_DB_RATE,
                    db_type=dbOper.ALL, host=DEFAULT_DB_HOST, port=DEFAULT_DB_PORT,
                    db_name=DEFAULT_DB_NAME, user=DEFAULT_DB_USER, passwd=DEFAULT_DB_PASSWD,
                    charset=DEFAULT_DB_CHARSET, mincached=DEFAULT_DB_MINCACHED, maxcached=DEFAULT_DB_MAXCACHED):
    return {
        'name' : name,
        'rate' : 100,
        'db_type' : db_type,
        'host' : host,
        'port' : 3306,
        'db_name' : db_name,
        'user' : user,
        'passwd' : passwd,
        'mincached' : mincached,
        'maxcached' : maxcached,
        'charset' : charset
    }

# configure db
dbConfigs.append(db_config_maker())

######### DBConfig end  ##########


# redis config
REDIS_PORT1 = 6379
DEFAULT_HOST = 'localhost'
# DEFAULT_HOST = 'redis'
#         DEFAULT_HOST = 'r-m5ef8971af1a9f54.redis.rds.aliyuncs.com'
#         REDIS_PASSWORD = "Qwe12345"


redis_configs = [{'host':DEFAULT_HOST, 'port' : REDIS_PORT1}]
MP_TOKEN = 'mp_token'
MP_TOKEN_LOCK = 'mp_token_lock'

APPID = "wxd0b09445bfc46d53"
AUTH_BASE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APPID + "&redirect_uri=http%3A%2F%2Fhackday.bingyan.net%2Flogin&response_type=code&scope=snsapi_userinfo&state=public/"
# hustbbm
APPSECRET = "212c139737fbe2602f0cbe766b96b161"
ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + APPID + "&secret=" + APPSECRET
USER_LIST_URL = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s"
USER_DETAIL_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"
TEMPLATE_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"
SEND_MSG_URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s"

WEB_ACCESS_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + APPID + "&secret=" + APPSECRET + "&code=%s&grant_type=authorization_code"
USER_BASE_INFO_URL = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"
