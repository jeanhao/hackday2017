#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年2月26日

@author: zenghao
'''
import gevent
from gevent.greenlet import Greenlet
import time


class DelayObject:
    """延迟调用对象\n
    """

    def __init__(self, f, *args, **kw):
        """
        @param f: function f是一个function对象\n
        @param args: f的必要参数\n
        @param kw: f的可选参数\n
        """
        self.f = f
        self.args = args
        self.kw = kw

    def call(self):
        """调用执行函数，并且返回结果\n
        """
        return self.f(*self.args, **self.kw)

class DelayCall(Greenlet):

    def __init__(self, seconds, f, *args, **kw):
        """以一个微线程的方式实现一个定时器\n
        """
        Greenlet.__init__(self)
        self.seconds = seconds
        self.delay_call = DelayObject(f, *args, **kw)

    def cancel(self):
        """取消定时器\n
        """
        self.kill()

    def _run(self):
        """通过sleep进行延迟调用注册的函数,这里的sleep与线程的sleep不同，他是基于微线程的\n
        """
        gevent.sleep(self.seconds)
        return self.delay_call.call()

class LoopingCall(Greenlet):

    """以一个微线程的方式实现一个定时调用 example:
    def p(x):
        print x
    lc = LoopingCall(2, 5, p, "xx")
    lc.start() # 2s后会执行 d._run
    # some condition
    lc.cancel()
    """

    def __init__(self, delayTime, interval, f, *args, **kw):
        Greenlet.__init__(self)
        self.interval = interval
        self.delayCall = DelayCall(delayTime, self._delayStart)
        self.delay = DelayObject(f, *args, **kw)


    def cancel(self):
        """取消定时调用
        """
        self.kill()

    def _delayStart(self):
        while True:
            gevent.sleep(self.interval)
            self.delay.call()

    def _run(self):
        self.delayCall.start()

class Timeout(object):
    """example:
    def p(x):
        print x
    t = Timeout(4, p, "xx")
    # 如果在4s内没有调用t.reset, 则会触发p被调用
    """
    def __init__(self, seconds, cb, *args, **kw):
        """
        """
        self.seconds = seconds
        self.cb = cb
        self.args = args
        self.kw = kw
        self.dc = DelayCall(seconds, cb, *args, **kw)
        self.dc.start()

    def cancel(self):
        self.dc.cancel()

    def reset(self):
        """要在要进行超时设置的函数里调用, 也可以使用其它方式(如继承)
        """
        self.dc.cancel()
        self.dc = DelayCall(self.seconds, self.cb, *self.args, **self.kw)
        self.dc.start()

if __name__ == '__main__':
    def printHello(x):
        print "hello", x
    lc = LoopingCall(1, 0.5, printHello, "zenghao")
    lc.start()
    print '12'
    while True:
#         time.sleep(99999)
        gevent.sleep(5)
        print "1111"
