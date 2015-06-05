# -*- coding: utf-8 -*-
'''
Created on May 26, 2015

@author: chenchen
'''

import Queue
import sys
import thread
import time

from threadpool import makeRequests

from CommonLib import callCommandBySubprocess
from DeviceManager import DeviceManager
from Singleton import singleton
from TestcaseResultDao import TestcaseResultDao
from ThreadPoolManager import ThreadPoolManager


@singleton
class TestcaseManager:
    def __init__(self):
        self.queue = Queue.Queue()
        thread.start_new_thread(self._processOnBackground, ())
        
    def _processOnBackground(self):
        while True:
            if self.queue.empty():
                time.sleep(1)
                continue
            
            testcase = self.queue.get()
            deviceInfo = DeviceManager().shiftDevice(testcase.condition)
            if not deviceInfo:
                self.queue.put(testcase)
                
                time.sleep(1)
                continue
            
            requests = makeRequests(self._runTestcase, [{'deviceInfo':deviceInfo, 'testcase':testcase}])
            [ThreadPoolManager().threadPool.putRequest(req) for req in requests]
            ThreadPoolManager().threadPool.wait()
    
    ''' 增加工作请求，将请求加入到工作队列中 '''
    def process(self, testcase):
        self.queue.put(testcase)
        
    def _runTestcase(self, *args, **kwds):
        try:
            deviceInfo = args[0]['deviceInfo']
            testcase = args[0]['testcase']
            testcaseResult = testcase.testcaseResult

            TestcaseResultDao().insert(testcaseResult)
            
            uninstallCommand = "adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package)
            sys.stderr.write(uninstallCommand)
            uninstallCommandLines = callCommandBySubprocess(uninstallCommand)
            TestcaseResultDao().update(testcaseResult, uninstallCommandLines)
            
            installCommand = "adb -s %s install %s" % (deviceInfo.serial, testcase.apkpath)
            sys.stderr.write(installCommand)
            installComandLines = callCommandBySubprocess(installCommand)
            TestcaseResultDao().update(testcaseResult, installComandLines)
            
            for prepare in testcase.prepares:
                prepare = self._replaceMacro(prepare, deviceInfo, testcase);
                prepareLines = callCommandBySubprocess(prepare)
                TestcaseResultDao().update(testcaseResult, prepareLines)
                
            for command in testcase.commands:
                command = self._replaceMacro(command, deviceInfo, testcase);
                commandLines = callCommandBySubprocess(command)
                TestcaseResultDao().update(testcaseResult, commandLines)
                
            postUninstallCommandLines = callCommandBySubprocess("adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package))
            TestcaseResultDao().update(testcaseResult, postUninstallCommandLines)
            
            testcaseResult.isEnd = 1
            testcaseResult.isSuccess = 1
            TestcaseResultDao().update(testcaseResult)
        finally:
            DeviceManager().resetDevice(deviceInfo)
            
    def _replaceMacro(self, original, deviceInfo, testcase):
        original = original.replace("${SERIAL}", deviceInfo.serial)
        original = original.replace("${WORKSPACE}", testcase.testcasepath[0:testcase.testcasepath.rindex('/')])
        
        return original