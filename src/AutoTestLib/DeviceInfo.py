#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DeviceInfo.py
"""
Created on 2015年1月5日
Func: 手机信息类，保存手机需要的所有信息，方便后期维护
@author: sqxu
"""


import os
import time
import platform

from CommonLib import callCommand

TYPE_OF_SYSTEM = 'Linux'
if platform.system() == 'Linux':
    TYPE_OF_SYSTEM = 'Linux'
else:
    TYPE_OF_SYSTEM = 'Windows'

class DeviceInfo():
    '''
    保存手机基本信息，目前使用的信息有序列号和型号，后期会维护其他信息，如屏幕大小、分辨率等
    '''
    def __init__(self, ser, stat=1):
        '''
        @param serial: 序列号，手机的唯一标示
        @param product: 型号
        @param state: 手机状态，1为可用，-1为不可用
        '''
        self.serial = ser
        self.product = self.getProductBySerial()
        self.resolution = self.getResolutionBySerial()
        self.edition = self.getEditionBySerial()
        self.memory_size, self.memory_free = self.getMemoryParameterBySerial()
        self.sim_state = self.getSimStateBySerial()
        self.state = stat
        self.first_install = True

    def getProductBySerial(self):
        """
        根据手机序列号获取手机产品型号
        """
        product = ''
        try:
            pd = callCommand("adb -s %s shell getprop ro.product.model" % self.serial)[0].strip()
            product = pd
        except:
            pass

        return product

    def getResolutionBySerial(self):
        """
        获取手机分辨率
        """
        resolution = ''
        try:
            resolution_cmd = 'adb -s %s shell dumpsys display | grep DisplayDeviceInfo' % self.serial
            if TYPE_OF_SYSTEM == 'Windows':
                resolution_cmd = 'adb -s %s shell dumpsys display | findstr DisplayDeviceInfo' % self.serial
            rlt = callCommand(resolution_cmd)[0].strip()
            rlt = rlt[rlt.find(':')+1:rlt.find('}')].split(',')[0].strip()
            resolution = rlt
        except:
            pass

        return resolution

    def getEditionBySerial(self):
        """
        获取手机安卓版本信息
        """
        android_edition = ''
        try:
            edition = callCommand('adb -s %s shell getprop ro.build.version.release' % self.serial)[0].strip()
            android_edition = edition
        except:
            pass

        return android_edition

    def getMemoryParameterBySerial(self):
        """
        获取手机内存信息，返回内存大小和可用内存大小
        """
        memory_size = ''
        memory_free = ''
        try:
            cmd = 'adb -s %s shell df | grep data' % self.serial
            if TYPE_OF_SYSTEM == 'Windows':
                cmd = 'adb -s %s shell df | findstr data' % self.serial

            memory_result = callCommand(cmd)[0].strip().split()
            memory_size = memory_result[1]
            memory_free = memory_result[3]
        except:
            pass

        return memory_size, memory_free

    def getSimStateBySerial(self):
        """
        判断手机是否插入sim卡，主要根据imsi号进行判断
        """
        sim_state = 0
        try:
            cmd = 'adb -s %s shell dumpsys telephony.registry | grep mServiceState' % self.serial
            if TYPE_OF_SYSTEM == 'Windows':
                cmd = 'adb -s %s shell dumpsys telephony.registry | findstr mServiceState' % self.serial
            service_state = callCommand(cmd)[0].strip().split()[0].split('=')[1]
            if int(service_state) == 0:
                sim_state = 1
            else:
                sim_state = 0
        except:
            pass

        return sim_state

    def pullFileFromDevice(self, resource_file, target_path):
        """
        将手机中的文件保存至电脑中
        """
        cmd = 'adb -s %s pull %s %s' % (self.serial, resource_file, target_path)
        callCommand(cmd)

    def pushFileToTargetPath(self, resource_file, target_path):
        """
        将源文件拷贝至指定手机上的目标路径下
        @:param resource_file: 源文件位置
        @:param target_path: 目标路径
        @:param serial：手机序列号
        """
        cmd = 'adb -s %s push %s %s' % (self.serial, resource_file, target_path)
        callCommand(cmd)

    def pushDocumentToDevice(self, local_document, target_document):
        """
        将本地文件夹传入手机中对应的文件夹，且按照本地文件夹的结构传入新文件夹
        """
        file_list = os.listdir(local_document)
        for sub_file in file_list:
            local_file = os.path.join(local_document, sub_file)
            if os.path.isfile(local_file):
                self.pushFileToTargetPath(local_file, target_document + '/' + sub_file)
            else:
                self.pushDocumentToDevice(local_file, target_document + '/' + sub_file)

    def installApk(self, apk_path, uni_apk_path):
        """
        安装apk，并且返回安装的相关结果
        """
        is_success = False
        rslt_info = {}
        uninstall = 'adb -s %s uninstall %s' % (self.serial, uni_apk_path)
        install = 'adb -s %s install %s' % (self.serial, apk_path)

        uni_time = time.time()
        try:
            if callCommand(uninstall)[-1].find('Success') >= 0:
                rslt_info['uni_time'] = time.time()-uni_time
        except:
                pass
        ins_time = time.time()
        try:
            if callCommand(install)[-1].find('Success') >= 0:
                rslt_info['ins_time'] = time.time()-ins_time
                is_success = True
        except:
            pass

        return is_success, rslt_info

    def setState(self, cur_state):
        self.state = cur_state

    def getState(self):
        return self.state

    def updateFirstInstallInfo(self):
        self.first_install = False


if __name__ == '__main__':
    de = DeviceInfo("MSM8625QSKUD")
    de.pushDocumentToDevice('D:\lingxi', '/sdcard/lingxitest')
    # print de.getMemoryParameterBySerial()
    # print de.getSimStateBySerial()
