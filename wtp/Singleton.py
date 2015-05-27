# -*- coding: utf8 -*-
'''
Created on May 25, 2015

@author: chenchen
'''

def singleton(self, *args, **kw):
    ''' singleton annotation '''  
    instances = {}  
    def _singleton():  
        if self not in instances:  
            instances[self] = self(*args, **kw)  
        return instances[self]  
    return _singleton  