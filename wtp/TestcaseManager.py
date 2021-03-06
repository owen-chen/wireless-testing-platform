# -*- coding: utf-8 -*-
'''
Created on May 26, 2015

@author: chenchen
'''

import Queue
import json
import thread
import time

from threadpool import makeRequests

from CommonLib import callCommand
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
            testcase.testcaseResult.deviceInfo = json.dumps(deviceInfo.toDict())

            TestcaseResultDao().insert(testcase.testcaseResult)
            
            uninstallCommand = "adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package)
            TestcaseResultDao().update(testcase.testcaseResult, callCommand(uninstallCommand))
            
            installCommand = "adb -s %s install %s" % (deviceInfo.serial, testcase.apkpath)
            TestcaseResultDao().update(testcase.testcaseResult, callCommand(installCommand))
            
            for prepare in testcase.prepares:
                prepare = self._replaceMacro(prepare, deviceInfo, testcase);
                TestcaseResultDao().update(testcase.testcaseResult, callCommand(prepare))
                
            for command in testcase.commands:
                command = self._replaceMacro(command, deviceInfo, testcase);
                TestcaseResultDao().update(testcase.testcaseResult, callCommand(command))
                
            TestcaseResultDao().update(testcase.testcaseResult, callCommand("adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package)))
            
            testcase.testcaseResult.isEnd = 1
            testcase.testcaseResult.isSuccess = 1
            TestcaseResultDao().update(testcase.testcaseResult)
        finally:
            DeviceManager().resetDevice(deviceInfo)
            
    def _replaceMacro(self, original, deviceInfo, testcase):
        original = original.replace("${SERIAL}", deviceInfo.serial)
        original = original.replace("${WORKSPACE}", testcase.testcasepath[0:testcase.testcasepath.rindex('/')])
        
        return original