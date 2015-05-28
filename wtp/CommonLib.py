# -*- coding: utf8 -*-
"""
Created on Dec 5, 2014

@author: chenchen
"""
import os
import subprocess
import sys


def ciWrite(tag, info=''):
    '''
            显示关键信息
    '''
    sys.stderr.write('##%s##%s\n'.decode('utf8').encode('gbk') % (tag, info))
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