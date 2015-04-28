#!/usr/bin/env python
# -*- coding: utf8 -*-
# CommondLib.py
"""
Created on 2014年12月5日
Func: 公共接口
@author: sqxu
"""
import os
import sys
import subprocess


def ciWrite(tag, info = ''):
    '''
            显示关键信息
    '''
    sys.stderr.write('##%s##%s\n'.decode('utf8').encode('gbk')%(tag, info))
    sys.stderr.flush()

    
def callCommand(cmd):
    '''
            执行命令并返回该命令的输出
    '''
    return os.popen(cmd).readlines()


def callCommandBySubprocess(command):
    """
            执行命令并返回该命令的输出，支持中文命令
    """
    return subprocess.check_output(command)


def getCaseName(test_case):
    """
    根据测试用例解析用例名字
    """
    try:
        split_list = test_case.split('#')[1]
        return split_list.split()[0]
    except:
        return "DEFAULTTEST"


# ----------------------功能验证-----------------------
if __name__ == '__main__':
    pass
