# -*- coding: utf-8 -*-    

import threading

from DBUtils.PooledDB import PooledDB
import pymysql

from app.utils.MyLogger import MyLoggerFactory


class DBModel():
    
    def __init__(self, dbConfig, readonly=False):
        self.dbConfig = dbConfig
        self.readonly = readonly
        self.logger = MyLoggerFactory().getLogger("dbManager")
        self.local = threading.local()
        self.local.conn = None
#         self._db_pool = self._initPool()
        
    def _initPool(self):                
        return  PooledDB(pymysql,
            host=self.dbConfig['host'],
            user=self.dbConfig['user'],
            passwd=self.dbConfig['passwd'],
            db=self.dbConfig['db_name'],
            port=int(self.dbConfig['port']),
            charset=self.dbConfig['charset'],
            mincached=self.dbConfig.get('mincached', 1) ,
            maxcached=self.dbConfig.get('maxcached', 20) ,
            cursorclass=self.dbConfig.get('self.local.cursorclass', pymysql.cursors.DictCursor),
            use_unicode=False,
        ) 
        
    def connect(self):
        self.local.conn = pymysql.connect(
                host=self.dbConfig['host'],
                user=self.dbConfig['user'],
                passwd=self.dbConfig['passwd'],
                db=self.dbConfig['db_name'],
                port=int(self.dbConfig.get('port', 3306)),
                charset=self.dbConfig.get('charset', 'utf8'),
                cursorclass=self.dbConfig.get('self.local.cursorclass', pymysql.cursors.DictCursor),
            )
#         self.local.conn = self._db_pool.connection()
        return self.local.conn
    
    # 执行sql语句
    def execute(self, sql, options=None):
        if options != None:
            sqls = self._generateSqls(sql, options)
            for sql in sqls:
                self.local.cursor.execute(sql)
        else:
            self.local.cursor.execute(sql)
        return self.local.cursor
    
    def executemany(self, sql, params, options=None):
        if options != None:
            sqls = self._generateSqls(sql, options)
            for sql in sqls:
                self.local.cursor.executemany(sql, params)
        else:
            self.local.cursor.executemany(sql, params)
        return self.local.cursor
    # 获取单条数据
    def GetOne(self, sql, options=None, connected=False):
        result_one = {}
        sqls = self._generateSqls(sql, options)
        for sql in sqls:
            if self.execute(sql) != None:
                result_one = self.local.cursor.fetchone()
                if result_one and len(result_one) > 0:
                    break
        return result_one
        
    # 获取数据列表
    def GetList(self, sql, options=None, connected=False):
        result_list = []
        limit_count = options and options.get('limit_count')
        sqls = self._generateSqls(sql, options)
        for sql in sqls:
            if self.execute(sql) != None:
                result_list.extend(self.local.cursor.fetchall())
                if limit_count and len(result_list) >= limit_count:
                    # 有指定数量限制
                    result_list = result_list[:options['limit_count']]
                    break
        return result_list
        
    def _generateSqls(self, sql, options=None):
        if options == None or "##TABLE_INDEX##" not in sql:
            return [sql]
            
        if options.get('table_index') != None:
            return [sql.replace("##TABLE_INDEX##", str(options['table_index']))]
        elif options.get('table_count') != None:
            sqls = []
            if options.get('desc', True) == True:
                range_count = range(options['table_count'] - 1, -1, -1)
            else:
                range_count = range(0, options['table_count'])
            for table_index in range_count:
                sqls.append(sql.replace("##TABLE_INDEX##", str(table_index)))
            return sqls
        else:
            return [sql]

    
