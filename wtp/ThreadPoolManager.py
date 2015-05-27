# -*- coding: utf8 -*-
'''
Created on 2014年12月16日
@author: sqxu
@author: chenchen9
'''

import threadpool

from DeviceManager import DeviceManager
from Singleton import singleton


@singleton
class ThreadPoolManager: 
    '''
        线程池管理者，负责工作队列，结果队列和工作线程的创建，并且完成对线程的管理
        @param thread_number: 线程池线程数
        @param timeout: 执行测试用例超时时间
        @param _work_queue: 工作求情队列
        @param _result_queue: 结果队列，与工作队列都是线程安全的
        @param _failed_queue: 保存执行失败的测试用例
        @param _work_threads: 工作线程列表
        @param _devices_list: 手机信息列表
        @param _result_thread: 用于展示结果的线程
    ''' 
    def __init__(self):
#         self._work_queue = Queue.Queue() 
#         self._result_queue = Queue.Queue()
#         self._failed_queue = Queue.Queue()
#         self._time_out = 5 * 60 * 1000
#         self._work_threads = []
#         self._result_cond = threading.Condition()
#         self._result_thread = AnalysisResultThread.AnalysisResultThread(self._result_queue, result_path, \
#                                                                         self._dvc_event, self._result_cond, \
#                                                                         getRsltFunc)
#         self.createThreads(runTestCase, prepareWorkForDevice, prepareWorkForCase)
        self.threadNumber = len(DeviceManager().getDeviceInfoList().available_device_list) * 2
        self.threadPool = threadpool.ThreadPool(self.threadNumber)