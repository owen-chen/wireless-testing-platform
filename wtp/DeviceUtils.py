# -*- coding: utf-8 -*-
'''
Created on May 21, 2015

@author: chenchen
'''
import os
import time

from CommonLib import callCommand


class DeviceUtils:
    """ 根据手机序列号获取手机产品型号 """
    @staticmethod
    def getProductBySerial(serial):
        return callCommand("adb -s %s shell getprop ro.product.model" % serial)[0].strip()
    
    """ 获取手机分辨率 """
    @staticmethod
    def getResolutionBySerial(serial):
        resolution_cmd = 'adb -s %s shell dumpsys display | grep DisplayDeviceInfo' % serial
        rlt = callCommand(resolution_cmd)[0].strip()
        return rlt[rlt.find(':') + 1:rlt.find('}')].split(',')[0].strip()
    
    """ 获取手机安卓版本信息 """
    @staticmethod
    def getEditionBySerial(serial):
        return callCommand('adb -s %s shell getprop ro.build.version.release' % serial)[0].strip()
    
    """ 获取手机内存信息，返回内存大小和可用内存大小 """
    @staticmethod
    def getMemoryParameterBySerial(serial):
        memory_result = callCommand('adb -s %s shell df | grep data' % serial)[0].strip().split()
        return memory_result[1], memory_result[3]

    """ 判断手机是否插入sim卡，主要根据imsi号进行判断 """
    @staticmethod
    def getSimStateBySerial(serial):
        service_state = callCommand('adb -s %s shell dumpsys telephony.registry | grep mServiceState' % serial)[0].strip().split()[0].split('=')[1]
        return int(service_state) == 0;
    
    """ 将手机中的文件保存至电脑中 """
    @staticmethod
    def pullFileFromDevice(serial, source, target):
        callCommand('adb -s %s pull %s %s' % (serial, source, target))

    """ 将源文件拷贝至指定手机上的目标路径下 """
    @staticmethod
    def pushFileToTargetPath(serial, source, target):
        callCommand('adb -s %s push %s %s' % (serial, source, target))

    """ 将本地文件夹传入手机中对应的文件夹，且按照本地文件夹的结构传入新文件夹 """
    @staticmethod
    def pushFolderToDevice(serial, source, target):
        file_list = os.listdir(source)
        for sub_file in file_list:
            local_file = os.path.join(source, sub_file)
            if os.path.isfile(local_file):
                DeviceUtils.pushFileToTargetPath(serial, local_file, target + '/' + sub_file)
            else:
                DeviceUtils.pushFolderToDevice(serial, local_file, target + '/' + sub_file)

    """ 安装apk，并且返回安装的相关结果 """
    @staticmethod
    def installApk(serial, apk_path, uni_apk_path):
        is_success = False
        rslt_info = {}
        uninstall_command = 'adb -s %s uninstall_command %s' % (serial, uni_apk_path)
        install_command = 'adb -s %s install_command %s' % (serial, apk_path)

        uni_time = time.time()
        if callCommand(uninstall_command)[-1].find('Success') >= 0:
            rslt_info['uni_time'] = time.time() - uni_time

        ins_time = time.time()
        if callCommand(install_command)[-1].find('Success') >= 0:
            rslt_info['ins_time'] = time.time() - ins_time
            is_success = True

        return is_success, rslt_info