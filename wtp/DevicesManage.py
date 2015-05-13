#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DevicesManage.py
"""
Created on 2014年12月18日
@author: sqxu
"""

from DeviceInfo import DeviceInfo
from CommonLib import callCommand, ciWrite

        
class DevicesManage():
    """
    对手机的整体管理，包括获取手机信息列表、打印手机信息等
    """
    def getDevicesList(self):
        """
        获取与测试服务器链接的手机信息，保存在列表中
        手机信息包括serial，priduct和state等
        state初始默认为1，即代表该机器可用，-1代表不可用
        """
        devices_list = []
        unable_list = []
        try:
            adb_dvc = callCommand("adb devices")[1:]
            for dvc_info in adb_dvc:
                if dvc_info.strip():
                    serial = dvc_info.split()[0]
                    if dvc_info.split()[1] != 'device':
                        unable_list.append((serial, dvc_info.split()[1]))
                        continue
                    try:
                        dvc = DeviceInfo(serial)
                        devices_list.append(dvc)
                    except:
                        continue
        except:
            pass
                
        return devices_list, unable_list

    def printDevicesInfo(self, devices_list, unable_list):
        fmt = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s'
        ciWrite('DEVICE_STATUS', fmt % ('serial', 'product', 'device_state', 'resolution', 'edition', 'memory_state', 'sim_state'))

        for devc in devices_list:
            ciWrite('DEVICE_STATUS', fmt % (devc.serial, devc.product, 'device', devc.resolution, devc.edition, \
                                            (devc.memory_size + '/' +devc.memory_free), devc.sim_state))

        for dvc in unable_list:
            ciWrite('DEVICE_STATUS', fmt % (dvc[0], '', dvc[1], '', '', '', ''))

    def pushDocumentToAllDevices(self, local_document, target_document):
        pass


# -------------------功能验证部分-----------------------
if __name__ == '__main__':
    import os
    install = 'adb install C:\Users\sqxu\PycharmProjects\AutoTestLib\IME\apk\iFlyIME_v5.0.1740.apk'
    print os.popen(install).readlines()
