# -*- coding: utf-8 -*-
"""
Created on Jan 5, 2015
@author: sqxu
@author: chenchen
"""
from DeviceUtils import DeviceUtils


class DeviceInfo():
    ''' 保存手机基本信息，目前使用的信息有序列号和型号，后期会维护其他信息，如屏幕大小、分辨率等 '''
    '''
    @param serial: 序列号，手机的唯一标示
    @param state: 手机状态，1为可用，-1为不可用
    '''
    def __init__(self, serial, state=True):
        self.serial = serial
        self.state = state
        self.first_install = True
        if state:
            self.product = DeviceUtils.getProductBySerial(serial)
            self.resolution = DeviceUtils.getResolutionBySerial(serial)
            self.edition = DeviceUtils.getEditionBySerial(serial)
            self.memory_size, self.memory_free = DeviceUtils.getMemoryParameterBySerial(serial)
            self.sim_state = DeviceUtils.getSimStateBySerial(serial)
            
    def toDict(self):
        device_info_dict = {}
        device_info_dict['serial'] = self.serial
        device_info_dict['product'] = self.product
        device_info_dict['resolution'] = self.resolution
        device_info_dict['edition'] = self.edition
        device_info_dict['memory_size'] = self.memory_size
        device_info_dict['memory_free'] = self.memory_free
        device_info_dict['sim_state'] = self.sim_state
        device_info_dict['first_install'] = self.first_install
        device_info_dict['state'] = self.sim_state
        return device_info_dict
