#!/usr/bin/env python
# -*- coding: utf-8 -*-
#ProcessLock.py
'''
Created on 2014年12月31日
Func: 文件锁，防止多个用户启动程序导致手机复用出现的异常情况
@author: sqxu
'''

import os
try:  
    import fcntl  
    FILE_NAME = '/home/cis/processlock.pid'
    LOCK_EX = fcntl.LOCK_EX  
except ImportError:  
    # Windows平台下没有fcntl模块  
    fcntl = None  
    import win32con
    import win32file  
    import pywintypes  
    FILE_NAME = 'C:\\processlock.pid'
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK  
    overlapped = pywintypes.OVERLAPPED()  
  
class Lock:  
    """
            进程锁 ，利用锁定文件的方法实现
    """  
    def __init__(self):  
        self._file_name = FILE_NAME  
        #-------------如果文件不存在则创建  
        self._handle = open(FILE_NAME, 'w')

    def acquire(self):  
        #-------------文件上锁  
        if fcntl:  
            fcntl.flock(self._handle, LOCK_EX)  
        else:  
            hfile = win32file._get_osfhandle(self._handle.fileno())  
            win32file.LockFileEx(hfile, LOCK_EX, 0, -0x10000, overlapped)  
  
    def release(self):  
        #-------------文件解锁  
        if fcntl:  
            fcntl.flock(self._handle, fcntl.LOCK_UN)  
        else:  
            hfile = win32file._get_osfhandle(self._handle.fileno())  
            win32file.UnlockFileEx(hfile, 0, -0x10000, overlapped)  
  
    def __del__(self):  
        try:  
            self._handle.close()  
            os.remove(self._file_name)
        except:
            pass

#------------------测试部分
if __name__ == '__main__':  
    # 测试：依次运行本程序多个实例，第N个实例运行耗时是第一个的N倍  
    import time  
    print 'Time: %s' % time.time()  
  
    lock = Lock()  
    try:  
        lock.acquire()  
        time.sleep(20)  
    finally:
        lock.release()  
    
    print 'Time: %s' % time.time() 
