# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: chenchen
'''
import os
import uuid

import lazyxml

from Configuration import Configuration
from Testcase import Testcase


class TestcaseReader:
    def __init__(self, apkpath, projectname):
        self.apkpath = apkpath
        self.projectname = projectname
        self.uuid = self.projectname + "-" + uuid.uuid4()
        
        self.testcaseList = []
        
        self._load();
        
    ''' 确定测试用例文件路径 '''
    def _getTestcasePath(self):
        tempPath = self.projectname.replace("-", "/")

        while True:
            testcasePath = "%s/%s/testcase.xml" % (Configuration().dicts['testcase']['testcaseServer'], tempPath)
            exist = os.path.isfile(testcasePath)
            if exist:
                return testcasePath
            
            if (tempPath.find('/') == -1 and tempPath.find('_') == -1) or not tempPath:
                raise Exception
            if tempPath.find('_') != -1:
                tempPath = tempPath[:tempPath.rindex('_')]
            else:
                tempPath = tempPath[:tempPath.rindex('/')]

        raise Exception
    
    def _load(self):
        xml = open(self._getTestcasePath()).read()
        dicts = lazyxml.loads(xml, strip=False)
        
        if not dicts or not dicts['testcases'] or not dicts['testcases']['testcase']:
            raise Exception("no testcase found")
        
        package = dicts['package']
        if type(dicts['testcases']['testcase']) is dict:
            self.testcaseList.append(self._readTestcase(dicts['testcases']['testcase'], package))
        else:
            for testcaseDict in dicts['testcases']['testcase']:
                self.testcaseList.append(self._readTestcase(testcaseDict, package))
                
    def _readTestcase(self, testcaseDict, package):
        if (not testcaseDict.has_key('name')) and (not testcaseDict.has_key('description')):
            raise Exception
        
        name = None
        if testcaseDict.has_key('name'):
            name = testcaseDict['name']
        else:
            name = testcaseDict['description']

        testcase = Testcase(name, self.apkpath.strip(), testcaseDict['description'].strip() if testcaseDict.has_key('description') else None, self.testcasePath.strip(), package.strip())
            
        testcase.testcaseResult.testcaseName = testcase.name
        testcase.testcaseResult.parentUuid = self.uuid
            
        if type(testcaseDict['commands']['command']) is list:
            for command in testcaseDict['commands']['command']:
                testcase.commands.extend(self.splitCommandLine(command))
        else:
            testcase.commands.extend(self.splitCommandLine(testcaseDict['commands']['command']))
            
        if testcaseDict.has_key('condition') and testcaseDict['condition'].has_key('sim'):
            testcase.condition.sim = True if testcaseDict['condition']['sim'].lower() != 'false' else False

        if type(testcaseDict['prepares']['prepare']) is list:
            for prepare in testcaseDict['prepares']['prepare']:
                testcase.prepares.extend(self.splitCommandLine(prepare))
        else:
            testcase.prepares.extend(self.splitCommandLine(testcaseDict['prepares']['prepare']))
        
        return testcase
    
    def splitCommandLine(self, command):
        command = command.strip()
        if command.find("\n") == -1:
            return [command.strip()]
        else: 
            return [x.strip() for x in command.split("\n")]
