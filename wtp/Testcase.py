# -*- coding: utf-8 -*-
'''
Created on May 25, 2015

@author: chenchen
'''

class Testcase:
    ''' test case model '''
    def __init__(self, apkpath, description, testcasepath, package):
        self.commands = []
        self.apkpath = apkpath
        self.prepares = []
        self.description = description
        self.testcasepath = testcasepath
        self.package = package
    
