#!/usr/bin/env python
# -*- coding: utf-8 -*-
#TestEntrance.py
"""
Created on 2015年1月22日
Func: 测试入口
@author: sqxu
"""

import sys

from CaseManage import CasesManage
from CommonLib import ciWrite
from Config import Config
from DevicesManage import DevicesManage
from ProcessLock import Lock
from SSHServer import SSHServer


def execScript(cfg_file, runTestCase, prepareWorkForDevice, prepareWorkForCase, getResult, apk_path=None):
    """
    外部调用入口，需传入配置文件路径，测试前准备工作函数以及工作函数
    @param prepareFunc: 测试前准备工作，可为空
    @param runFunc: 测试过程，不可为空
    @param getResultFunc: 结果处理，不可为空
    """
    lock = Lock()
    try:
        lock.acquire()
        # 判断是否链接有手机,没有可用手机,退出程序
        devc_mgr = DevicesManage()
        devices_list, unable_list = devc_mgr.getDevicesList()
        devc_mgr.printDevicesInfo(devices_list, unable_list)
        if (len(devices_list) == 0):
            ciWrite('ERROR', 'can\'t find test instance devices')
            sys.exit()

        # 获取配置文件
        cfg = Config(cfg_file, apk_path)

        # 从文件服务器上获取相关文件
        # SSHServer('172.16.95.14', 22, 'cis', 'cis', '/home/cis/auto-test/ime', 'd://ime ')
        
        # 执行测试
        CasesManage(cfg, devices_list, runTestCase, prepareWorkForDevice, prepareWorkForCase, getResult)
    finally:
        lock.release()
