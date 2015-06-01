# -*- coding: utf-8 -*-
'''
Created on May 25, 2015

@author: chenchen
'''
from Condition import Condition


class Testcase:
    ''' test case model '''
    def __init__(self, apkpath, description, testcasepath, package, condition=Condition()):
        self.commands = []
        self.apkpath = apkpath
        self.prepares = []
        self.description = description
        self.testcasepath = testcasepath
        self.package = package
        self.condition = condition
    
