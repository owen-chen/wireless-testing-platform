# -*- coding: utf-8 -*-
"""
Created on 2014年12月18日
@author: sqxu
@author: chenchen9
"""

import json
import random
import thread
from threading import Lock
import time

from CommonLib import callCommand, ciWrite
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
    
    def unshiftDevice(self):
        try:
            self._lock.acquire()
        
            available_device_len = len(self._deviceInfoList.available_device_list)
            if available_device_len <= 0:
                return None
            
            index = random.randint(0, available_device_len - 1)
            deviceInfo = self._deviceInfoList.available_device_list.pop(index)
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
        ciWrite('DEVICE_STATUS', json.dumps(self._deviceInfoList.toDict()))
