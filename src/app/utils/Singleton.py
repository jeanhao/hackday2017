#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Singleton(type):
    """Singleton Metaclass"""

    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance

from threading import Lock
class ThreadSafeSingleton(object):
    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None
        self._mutex = Lock()

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self._mutex.acquire()
            if self.instance is None:
                self.instance = super(Singleton, self).__call__(*args, **kwargs)
            self.__mutex.release()
        return self.instance

def singleton(cls, *args, **kw):
    instances = {}
    lock = Lock()
    def _singleton():
        if cls not in instances:
            lock.acquire()
            if cls not in instances:
                instances[cls] = cls(*args, **kw)
            lock.release()
        return instances[cls]
    return _singleton