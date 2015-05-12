#!/usr/bin/env python
# -*- coding: utf-8 -*-
#UpdateDeviceThread.py
'''
Created on 2014年12月26日
Func: 手机信息更新线程
@author: sqxu
'''
from threading import Thread
from CommonLib import ciWrite
from DevicesManage import DevicesManage


class UpdateDeviceThread(Thread):
    '''
            守护线程，定期调用adb命令，获取手机连接信息，并与已知的信息列表进行比较，
            如果存在差异则做出调整，保证工作线程中信息列表的准确性
            该线程设置为守护线程，主线程退出时该线程一起退出
    '''
    def __init__(self, devc_list, no_dvc_ent):
        '''
        @param _devc_list: 手机信息列表
        @param _dvc_event: 判断手否有手机连接的标志位
        @param _install_cond: 是否需要安装手机的condition
        '''
        super(UpdateDeviceThread, self).__init__()
        self.setDaemon(True) 
        self.setName('UpdateDeviceThread')
        self._devc_list = devc_list
        self._dvc_event = no_dvc_ent
        self._devices_mgr = DevicesManage()
    
    def run(self):
        '''
        获取当前最新的手机连接情况，保存在列表中，然后与之前的信息列表进行对比，如果有不同之处通知InstallApkThread安装apk
        '''
        err_tag = 0
        while True:
            try:
                devices_list, unable_list = self._devices_mgr.getDevicesList()
                # 如果发现没有手机连接，退出程序
                if len(devices_list) == 0:
                    err_tag = err_tag + 1
                    if err_tag > 2:
                        self._devc_list.clearList()
                        ciWrite('ERROR', '%s can\'t find any test instance devices' % self.getName())
                        self._dvc_event.set()
                        break
                    continue
                else:
                    err_tag = 0
                    # 根据当前获取的手机信息更新手机信息列表
                    self._devc_list.updateListByList(devices_list)
            except:
                pass
