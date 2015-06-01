# -*- coding: utf-8 -*-
"""
Created on Dec 18, 2014

@author: chenchen
"""

import json
import random
import thread
from threading import Lock
import time

from CommonLib import callCommand, write
from Condition import Condition
from DeviceInfo import DeviceInfo
from DeviceInfoList import DeviceInfoList
from DeviceUtils import DeviceUtils
from Singleton import singleton


@singleton
class DeviceManager():
    _deviceInfoList = None
    _lock = Lock()
    
    ''' singleton device manager '''
    def __init__(self):
        if self._deviceInfoList == None:
            self._deviceInfoList = DeviceInfoList()
            self.refresh(True)
            thread.start_new_thread(self._refreshPeriodly, ())
            
    def getDeviceInfoList(self):
        return self._deviceInfoList
    
    def shiftDevice(self, condition=Condition()):
        try:
            self._lock.acquire()
        
            available_device_len = len(self._deviceInfoList.available_device_list)
            if available_device_len <= 0:
                return None
            
            aimed_index = -1
            if condition.sim:
                ''' XXX loadbalance '''
                for i in range(len(self._deviceInfoList.available_device_list)):
                    available_device = self._deviceInfoList.available_device_list[i]
                    
                    if available_device.sim_state == condition.sim:
                        aimed_index = i
                        break
            else:
                aimed_index = random.randint(0, available_device_len - 1)
                
            if aimed_index == -1:
                return None
                
            deviceInfo = self._deviceInfoList.available_device_list.pop(aimed_index)
            DeviceUtils.lockDevice(deviceInfo.serial)
            
            return deviceInfo
        finally:
            self._lock.release()
#         
    def resetDevice(self, deviceInfo):
        try:
            self._lock.acquire()
            
            DeviceUtils.unlockDevice(deviceInfo.serial)
        finally:
            self._lock.release()
    
    def refresh(self, isFirst=False):
        tempAvailableDeviceList = []
        tempUnavailableDeviceList = []
        tempProcessingDeviceList = []
        
        try:
            self._lock.acquire()
            
            adb_dvc = callCommand("adb devices")[1:]
            for dvc_info in adb_dvc:
                try:
                    dvc_info = dvc_info.strip()
                    if not dvc_info:
                        continue
                    
                    serial = dvc_info.split()[0]
                    if dvc_info.split()[1] == 'device':
                        if isFirst:
                            DeviceUtils.unlockDevice(serial)
                        
                        if DeviceUtils.isDeviceLocked(serial):
                            tempProcessingDeviceList.append(DeviceInfo(serial))
                        else:
                            tempAvailableDeviceList.append(DeviceInfo(serial))
                    else:
                        tempUnavailableDeviceList.append(DeviceInfo(serial, False))
                except Exception, e:
                    print e
            
            self._deviceInfoList.available_device_list = tempAvailableDeviceList
            self._deviceInfoList.unavailable_device_list = tempUnavailableDeviceList
            self._deviceInfoList.processing_device_list = tempProcessingDeviceList
        finally:
            self._lock.release()
            
            
    def _refreshPeriodly(self):
        while True:
            self.refresh()
            time.sleep(1)

    def printDeviceInfoListToConsole(self):
        write('DEVICE_STATUS', json.dumps(self._deviceInfoList.toDict()))
