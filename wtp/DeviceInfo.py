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
