#!/usr/bin/env python
# -*- coding: utf8 -*-
#CaseManage.py
'''
Created on 2014年12月15日
@author: sqxu
'''
import os
import sys
import time
from CommonLib import callCommand, ciWrite
from ThreadPoolManage import ThreadPoolManage


class CasesManage():
    '''
            根据测试用例列表和手机信息列表进行测试，以达到最优任务调度
    '''
    def __init__(self, cfg, devc_list, runTestCase, prepareWorkForDevice, prepareWorkForCase, getResult):
        '''
        @param _config: 配置文件对象
        @param _devices_list: 手机信息列表
        @param _apk_path: apk路径
        @param _test_apk_path: 测试用apk路径
        @param _timeout: 单个测试用例超时时间
        @param _case_list: 测试用例列表
        @param _adb_mgr: adb命令对象，方便接口调用
        @param _threadpool: 线程池管理对象 
        '''
        self._apk_path = cfg.apk_path
        self._debug_store = cfg.debug_store
        self._apk_signed = cfg.apk_signed
        self._uni_apk_path = cfg.uni_apk_path
        self._time_out = cfg.thread_time_out
        self._install_apk = cfg.install_apk
        self._thread_numb = cfg.thread_numb
        self._devices_list = devc_list
        self._case_list = self._getCasesList(cfg.test_case_file)
        self._initSignedApk()
        self._result_path = self._getResultFilePath()
        self._thread_pool = ThreadPoolManage(self._thread_numb, self._devices_list, \
                                             self._time_out, self._result_path, \
                                             self._apk_path, self._uni_apk_path,\
                                             self._install_apk, getResult, \
                                             runTestCase, prepareWorkForDevice, \
                                             prepareWorkForCase)
        self._runTestCase()


    def _initSignedApk(self):
        '''
                        生成签名apk
                        并判断是否成功生成签名apk
        '''
        if not os.path.isfile(self._apk_path):
            ciWrite('ERROR', 'can\'t find %s file'%self._apk_path)
            sys.exit()
        
        #-------------判断是否需要签名
        if self._apk_signed:
            if not os.path.isfile(self._debug_store):
                ciWrite('ERROR', 'can\'t find %s file'%self._debug_store)
                sys.exit()
                
            apk_path_signed = self._apk_path + '_signed.apk'
            callCommand('jarsigner  -digestalg SHA1 -sigalg MD5withRSA -keystore %s -storepass android -keypass android -signedjar %s %s androiddebugkey'\
                        %(self._debug_store, apk_path_signed, self._apk_path))
        
            if not os.path.isfile(apk_path_signed):
                ciWrite('ERROR', 'signed apk not exist')
                sys.exit()
            else:
                self._apk_path = apk_path_signed
            
    def _getResultFilePath(self):
        '''
                        根据当前时间生成结果目录
        '''
        local_time = time.strftime('%Y-%m-%d-%H-%M',time.localtime())
        result_path = 'result_' + local_time
        #------------目录已经存在时，路径中加入秒，重新建立目录
        if os.path.isdir(result_path):
            local_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
            result_path = 'result_' + local_time
        
        return result_path
        
    def _getCasesList(self, case_file):
        '''
                        从测试用例的文件中获取测试用例
        '''
        if not os.path.isfile(case_file):
            ciWrite('ERROR', 'can\'t find %s file' % case_file)
            sys.exit()
        
        fp = open(case_file, 'r')
        lines = fp.readlines()
        case_list = []
        for line in lines:
            if(line.startswith('adb -s')):
                case_list.append(line.strip())
        fp.close()
        #--------------测试用例列表为空时退出
        if not len(case_list):
            ciWrite('ERROR', 'test cases is empty')
            sys.exit()

        return case_list

        
    def _runTestCase(self):
        '''
                        开启守护线程
                        将请求加到工作队列中并且开启结果展示线程
                        等待所有工作队列处理完成退出程序
        '''
        test_num = len(self._case_list)
        for i in range(test_num):
            t_case = self._case_list[i]
            self._thread_pool.addWorkRequest(t_case, i)

        self._thread_pool.startDeamonThread()

        ciWrite('TOTALCASENUM', str(test_num))
        self._thread_pool.startResultThread()
        self._thread_pool.waitAllComplete()


# -------------------test-------------------
if __name__ == "__main__":
    pass


