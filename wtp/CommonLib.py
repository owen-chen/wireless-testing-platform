# -*- coding: utf8 -*-
"""
Created on Dec 5, 2014

@author: chenchen
"""

import os
import subprocess
import sys


def write(tag, info=''):
    ''' 控制台输出 '''
    sys.stderr.write('##%s##%s\n'.decode('utf8').encode('gbk') % (tag, info))
    sys.stderr.flush()

    
''' 执行命令并返回该命令的输出 '''
def callCommand(cmd):
    return os.popen(cmd).readlines()


""" 执行命令并返回该命令的输出，支持中文命令 """
def callCommandBySubprocess(command):
    return subprocess.check_output(command)