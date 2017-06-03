# -*- coding: utf-8 -*-    
import redis,threading
from app.utils.Singleton import Singleton
from Configs import redis_configs
from app.utils.HashRing import HashRing

class RedisClient():
    
    __metaclass__ = Singleton
    def __init__(self):
        self.redis_models = {}
        for config in redis_configs:
            self.redis_models["%s:%s"%(config['host'],config['port'])] = self.create_redis_client(config['host'],config['port'])
        self.hash_ring = HashRing(self.redis_models.keys())
    
    def caller(self,method,key,*args,**kargs):
        return getattr(self.get_redis_client(key),method)(key,*args,**kargs)
    
    def get(self,key):
        return self.get_redis_client(key).get(key)
    
    def get_redis_client(self,key):
        return self.redis_models[self.hash_ring.get_node(key)]
    
#     @classmethod
#     def sel_model(cls,func):
#         def lazy_func(key,*args,**kargs):
#             cls.local.model = cls.get_redis_client(key)
#             return func(key,*args,**kargs)
#         return lazy_func()
    
    
    @staticmethod
    def create_redis_client(host = 'localhost',port = 6379):
        pool = redis.ConnectionPool(host=host,port=port)
        return redis.Redis(connection_pool = pool)
    
if __name__ == '__main__':
    redis = RedisClient.instance().caller
    print redis('set','key1','xixi')
    
    
    