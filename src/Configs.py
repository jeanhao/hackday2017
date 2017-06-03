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
DEFAULT_DB_NAME = 'dbserver'
DEFAULT_DB_USER = 'dbserver'
DEFAULT_DB_PASSWD = 'bulin'
DEFAULT_DB_CHARSET = 'utf8'
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
