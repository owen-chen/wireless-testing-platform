#!/usr/bin/env python
# -*- coding: utf8 -*-
#ThreadPoolManage.py
'''
Created on 2014年12月16日
@author: sqxu
'''

import Queue
import threading
import WorkRequestThread
import UpdateDeviceThread
import AnalysisResultThread
from MutexList import MutexList


class ThreadPoolManage: 
    '''
            线程池管理者，负责工作队列，结果队列和工作线程的创建，并且完成对线程的管理
    ''' 
    
    def __init__(self, thread_numb, devices_list, \
                  time_out, rslt_path, apk_apth, \
                  uin_apk_path, inst_apk, getRsltFunc, \
                  runTestCase, prepareWorkForDevice, \
                  prepareWorkForCase):
        '''
        @param thread_numb: 线程池线程数
        @param devices_list: 手机信息列表
        @param timeout: 执行测试用例超时时间
        @param _work_queue: 工作求情队列
        @param _result_queue: 结果队列，与工作队列都是线程安全的
        @param _failed_queue: 保存执行失败的测试用例
        @param _work_threads: 工作线程列表
        @param _devices_list: 手机信息列表
        @param _result_thread: 用于展示结果的线程
        @param _deamon_thread: 守护线程，用于手机信息的实时更新
        '''
        self._work_queue = Queue.Queue() 
        self._result_queue = Queue.Queue()  
        self._failed_queue = Queue.Queue()
        self._time_out = time_out  
        self._apk_apth = apk_apth
        self._uni_apk_path = uin_apk_path
        self._inst_apk = inst_apk
        self._work_threads = []
        self._devices_list = MutexList(devices_list)
        self._dvc_event = threading.Event()
        self._result_cond = threading.Condition()
        self._result_thread = AnalysisResultThread.AnalysisResultThread(self._result_queue, rslt_path, \
                                                                        self._dvc_event, self._result_cond, \
                                                                        getRsltFunc)
        self._update_thread = UpdateDeviceThread.UpdateDeviceThread(self._devices_list, self._dvc_event)
        self.createThreads(thread_numb, runTestCase, prepareWorkForDevice, prepareWorkForCase)
        
    def createThreads( self, thread_numb, runTestCase, prepareWorkForDevice, prepareWorkForCase):
        '''
                        生成工作线程，并保存在线程列表中
        '''
        for i in range(thread_numb):
            worker = WorkRequestThread.WorkRequestThread(self._work_queue, self._result_queue, \
                                                         self._devices_list, self._dvc_event, \
                                                         self._apk_apth, self._uni_apk_path, \
                                                         self._inst_apk, self._result_cond, \
                                                         runTestCase, prepareWorkForDevice, \
                                                         prepareWorkForCase)
            self._work_threads.append(worker)
   
    def waitAllComplete(self):
        '''
                        等待所有的线程都工作结束
        '''
        while len(self._work_threads):
            # 先判断异常标志位是否为真，为真是将工作队列情况,等所有线程都结束工作退出
            worker = self._work_threads.pop()
            worker.join()
            # 线程可用并且工作队列不为空，将线程重新加入列表中
            if worker.isAlive() and not self._work_queue.empty():  
                self._work_threads.append(worker)

    def addWorkRequest( self, *args, **kwds ):
        '''
                        增加工作请求，将请求加入到工作队列中
        '''
        self._work_queue.put((args, kwds))
        
    def startResultThread(self):
        '''
                        开启结果展示线程
        '''
        self._result_thread.start()
    
    def startDeamonThread(self):
        '''
                        开启守护线程
        '''
        self._update_thread.start()

    def getFailedCase(self):
        '''
                        从结果队列中获取结果，具体分析可根据不同需求进行处理
                        待进一步处理
        '''
        return self._failed_queue
            
# -----------测试部分------------------
if __name__ == '__main__':
    tpm = ThreadPoolManage()
