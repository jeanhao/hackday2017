# -*- coding: utf-8 -*-
import hashlib
from _collections import defaultdict

class HashRing(object):
    def __init__(self, nodes=None, n_number=100):
        """
        :param nodes:           所有的节点
        :param n_number:        一个节点对应多少个虚拟节点
        :return:
        """
        self._n_number = n_number   #每一个节点对应多少个虚拟节点，这里默认是3个
        self._node_dict = dict()    #用于将虚拟节点的hash值与node的对应关系
        self._sort_list = []        #用于存放所有的虚拟节点的hash值，这里需要保持排序
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """
        添加node，首先要根据虚拟节点的数目，创建所有的虚拟节点，并将其与对应的node对应起来
        当然还需要将虚拟节点的hash值放到排序的里面
        这里在添加了节点之后，需要保持虚拟节点hash值的顺序
        :param node:
        :return:
        """
        for i in xrange(self._n_number):
            node_str = "%s%s" % (node, i)
            key = self._gen_key(node_str)
            self._node_dict[key] = node
            self._sort_list.append(key)
        self._sort_list.sort()

    def remove_node(self, node):
        """
        这里一个节点的退出，需要将这个节点的所有的虚拟节点都删除
        :param node:
        :return:
        """
        for i in xrange(self._n_number):
            node_str = "%s%s" % (node, i)
            key = self._gen_key(node_str)
            del self._node_dict[key]
            self._sort_list.remove(key)

    def get_node(self, key_str):
        """
        返回这个字符串应该对应的node，这里先求出字符串的hash值，然后找到第一个小于等于的虚拟节点，然后返回node
        如果hash值大于所有的节点，那么用第一个虚拟节点
        :param :
        :return:
        """
        if self._sort_list:
            key = self._gen_key(key_str)
            for node_key in self._sort_list:
                if key <= node_key:
                    return self._node_dict[node_key]
            return self._node_dict[self._sort_list[0]]
        else:
            return None

    @staticmethod
    def _gen_key(key_str):
        """
        通过key，返回当前key的hash值，这里采用md5
        :param key:
        :return:
        """
        md5_str = hashlib.md5(key_str).hexdigest()
        return long(md5_str, 16)
    
if __name__ == '__main__':
    import string,random
    def gen_ramdon_string(length = 10):
        return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], length)).replace(' ','')

    hashRing = HashRing(["127.0.0.1", "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5", "192.168.1.6"])
    test_size = 10000
    str_dict = {}
    for i in xrange(test_size):
        ram_str = gen_ramdon_string()
        str_dict[ram_str] = hashRing.get_node(ram_str)
    
    host_count = defaultdict(int)
    for tup in  str_dict.values():
        host_count[tup] += 1
    print host_count
    hashRing.add_node('115.159.40.140')
    miss_num = 0
    new_dict= {}
    for key in str_dict:
        belong = hashRing.get_node(key)
        new_dict[key] = belong
        if  belong != str_dict[key]:
            miss_num += 1
    print 'miss num:',miss_num
    host_count = defaultdict(int)
    for tup in  new_dict.values():
        host_count[tup] += 1
    print host_count
