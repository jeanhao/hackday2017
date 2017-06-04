# -*- coding: utf-8 -*-
import redis, threading
from app.utils.Singleton import Singleton
from app.utils.HashRing import HashRing
from Configs import redis_configs
import time

class RedisClient():

    __metaclass__ = Singleton
    def __init__(self, timeout=0.1, expire=2):
        self.timeout = timeout  # 锁等待时间，防止线程饥饿
        self.expire = expire  # 锁超时时间，防止线程入锁后，无限执行等待
        self.lockExpireRecord = {}  # 若加锁，记录自己加的锁的超时时间，在解锁的时候先检查是否超时，若未超时再解锁

        self.redis_models = {}
        for config in redis_configs:
            self.redis_models["%s:%s" % (config['host'], config['port'])] = self.create_redis_client(config['host'], config['port'])
        self.hash_ring = HashRing(self.redis_models.keys())

    def caller(self, method, key, *args, **kargs):
        return getattr(self.get_redis_client(key), method)(key, *args, **kargs)

    def get(self, key):
        return self.get_redis_client(key).get(key)

    def get_redis_client(self, key):
        return self.redis_models[self.hash_ring.get_node(key)]

    # 分布式锁简单实现实现，防止缓存失效风暴
    def lock(self, lockKey):
        expire = time.time() + self.expire + 1
        lock = self.caller('set', lockKey, expire, ex=2, nx=True)  # 尝试通过设值获得锁，值为超时的绝对时间戳
        if lock:  # 拿到锁
            self.lockExpireRecord[lockKey] = expire
            return True
        else:  # 没拿到,查看是否已超时
            currentCacheExpire = self.caller("get", lockKey)
            if currentCacheExpire and time.time() > float(currentCacheExpire):  # 已经超时了
                oldCacheExpire = self.caller("getset", lockKey)  # 获取上一个锁到期时间，并设置现在的锁的到期时间
                if oldCacheExpire and oldCacheExpire == currentCacheExpire:  # 防止有误删，操作，假设有另一个线程也拿到了锁，这里会导致的old!=cur,
                    # 没有其它线程进行操作
                    return True
        return False

    def unlock(self, lockKey):
        if lockKey in self.lockExpireRecord and self.caller("get", lockKey) == self.lockExpireRecord[lockKey]:
            # 有记录且得到的锁是否是自己的才操作
            self.caller("delete", lockKey)
#     @classmethod
#     def sel_model(cls,func):
#         def lazy_func(key,*args,**kargs):
#             cls.local.model = cls.get_redis_client(key)
#             return func(key,*args,**kargs)
#         return lazy_func()


    @staticmethod
    def create_redis_client(host='localhost', port=6379):
        pool = redis.ConnectionPool(host=host, port=port)
        return redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    redis = RedisClient.instance().caller
    print redis('set', 'key1', 'xixi')


