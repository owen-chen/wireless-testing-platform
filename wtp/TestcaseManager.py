# -*- coding: utf-8 -*-
'''
Created on May 26, 2015

@author: chenchen
'''

import Queue
import thread
import time

from threadpool import makeRequests

from CommonLib import callCommand
from DeviceManager import DeviceManager
from Singleton import singleton
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
            
            deviceInfo = DeviceManager().shiftDevice()
            print deviceInfo
            if not deviceInfo:
                time.sleep(1)
                continue
            
            testcase = self.queue.get()
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
            
            print callCommand("adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package))
            print callCommand("adb -s %s install %s" % (deviceInfo.serial, testcase.apkpath))
            
            for prepare in testcase.prepares:
                prepare = self._replaceMacro(prepare, deviceInfo, testcase);
                print prepare
                print callCommand(prepare)
                
            for command in testcase.commands:
                command = self._replaceMacro(command, deviceInfo, testcase);
                print command
                print callCommand(command)
                
            print callCommand("adb -s %s uninstall %s" % (deviceInfo.serial, testcase.package))
        finally:
            DeviceManager().resetDevice(deviceInfo)
            
    def _replaceMacro(self, original, deviceInfo, testcase):
        original = original.replace("${SERIAL}", deviceInfo.serial)
        original = original.replace("${WORKSPACE}", testcase.testcasepath[0:testcase.testcasepath.rindex('/')])
        
        return original
        
    