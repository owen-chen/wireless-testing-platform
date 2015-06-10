# -*- coding: utf-8 -*-
'''
Created on May 22, 2015

@author: chenchen
'''
class DeviceInfoList:
    """
        获取与测试服务器链接的手机信息，保存在列表中
        手机信息包括serial，priduct和state等
        state初始默认为1，即代表该机器可用，-1代表不可用
    """
    def __init__(self):
        self.available_device_list = []
        self.unavailable_device_list = []
        self.processing_device_list = []
    
    def toDict(self):
        device_list_dict = {'device_list_count': 0, 'available_device_list':[], 'unavailable_device_list':[], 'processing_device_list': []}

        device_list_dict['device_list_count'] = len(self.available_device_list) + len(self.unavailable_device_list) + len(self.processing_device_list)

        for device_info in self.available_device_list:
            device_list_dict['available_device_list'].append(device_info.toDict())

        for device_info in self.processing_device_list:
            device_list_dict['processing_device_list'].append(device_info.toDict())

        for device_info in self.unavailable_device_list:
            device_list_dict['unavailable_device_list'].append(device_info.toDict())
        
        return device_list_dict
    
