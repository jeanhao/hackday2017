# -*- coding: utf-8 -*-    
import memcache


class MCClient():
    def __init__(self,hosts = ['localhost']):
        self.__mc = memcache.Client(hosts)
    
    def set(self, key, value,timeout = 43200):
        result = self.__mc.set(key,value)
        return result

    def get(self, key):
        name = self.__mc.get(key)
        return name

    def delete(self, key):
        result = self.__mc.delete(key)
        return result
    
    def touch(self,key,time=None):
        return self._mc.touch(key,time)
        
    def incr(self, key, delta=1):
        return self.__mc.incr(key, delta)
    
    def decr(self, key, delta=1):
        return self.__mc.decr(key, delta)
    
    def add(self, key, val, time=0):
        return self._mc.add(key,val,time)
    
    def append(self, key, val, time=0):
        return self._mc.append(key, val, time)
    
    def prepend(self, key, val, time=0):
        return self.__mc.prepend(key, val, time)
    
    def replace(self, key, val, time=0):
        return self.__mc.replace(key, val, time)
    
    def cas(self, key, val, time=0):
        return self.__mc.cas(key, val, time)
    
    def set_multi(self, mapping, time=0):
        return self.__mc.set_multi(mapping, time)
    
    def gets(self, key):
        return self.__mc.gets(key)
    
    def get_multi(self, keys):
        return  self.__mc.get_multi(keys)   
    
    def get_stats(self):
        return self.__mc.get_stats()
    
if __name__ == '__main__':
    mc = MCClient()
#         print mc.get('152_1473301792000')
#         slabs = mc.get_slabs()
#         for sever in slabs:
#             for index in sever[1]:
#                 for item in mc.get_stats('cachedump %s 10'%index):
#                     print item[1]
        
