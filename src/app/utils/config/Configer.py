#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Created on 2017年2月14日

@author: zenghao
'''
import json
class Configer(object):
    '''
    classdocs
    '''


    def __init__(self, configDict):
        '''
        Constructor
        '''
        self.file = configDict['file']
        self.section = configDict['section']
        self.name = configDict['name']
        self._rawValue = configDict['value']
        self.valueType = configDict['valueType']
        self.value = self.parseConfigByType()
    
    def parseConfigByType(self):
        if not self._rawValue:
            return {}
        if self.valueType == "json":
            return json.loads(self._rawValue)
        else:
            return self._rawValue
        
        