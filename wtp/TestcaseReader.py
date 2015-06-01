# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: chenchen
'''
import lazyxml

from Condition import Condition
from Testcase import Testcase


class TestcaseReader:
    def __init__(self, testcasePath, apkpath):
        self.testcasePath = testcasePath
        self.apkpath = apkpath
        self.testcaseList = []
        
        self._load();
    
    def _load(self):
        xml = open(self.testcasePath).read()
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
        testcase = Testcase(self.apkpath.strip(), testcaseDict['description'].strip(), self.testcasePath.strip(), package.strip())
            
        if type(testcaseDict['commands']['command']) is list:
            for command in testcaseDict['commands']['command']:
                testcase.commands.extend(self.splitCommandLine(command))
        else:
            testcase.commands.extend(self.splitCommandLine(testcaseDict['commands']['command']))
            
        print "<>", testcaseDict['condition']
        if testcaseDict['condition']:
            if testcaseDict['condition']['sim']:
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
