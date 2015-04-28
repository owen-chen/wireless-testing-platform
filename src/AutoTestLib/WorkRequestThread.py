#!/usr/bin/env python
# -*- coding: utf-8 -*-
#WorkThread.py
"""
Created on 2014年12月26日
Func: 工作请求处理线程
@author: sqxu
"""
import time
import Queue
from threading import Thread


class WorkRequestThread(Thread):  
    '''
            工作线程
            单个线程的工作内容，从工作队列中获取相关参数后，获取可用手机，执行测试用例
    '''
    queue_timeout = 5
    def __init__( self, work_queue, result_queue, \
                  devices_list, no_dvc_ent, \
                  apk_path, uni_path, \
                  inst_apk, rslt_cond, \
                  runTestCaseFunc, prepareWorkForDeviceFunc, \
                  prepareWorkForCaseFunc):
        '''
        @param _work_queue:  工作队列
        @param _result_queue: 结果队列 
        @param _failed_queue: 保存失败用例的队列
        @param _devices_list: 记录手机状态
        @param _devicelock: 手机信息列表锁
        '''
        super(WorkRequestThread, self).__init__()
        self._work_queue = work_queue  
        self._result_queue = result_queue 
        self._devices_list = devices_list 
        self._dvc_event = no_dvc_ent
        self._apk_path = apk_path
        self._uni_path = uni_path
        self._install_apk = inst_apk
        self._result_cond = rslt_cond
        self.runTestCase = runTestCaseFunc
        self.prepareWorkForDevice = prepareWorkForDeviceFunc
        self.prepareWorkForCase = prepareWorkForCaseFunc
        
        self.start()
        
    def getPhoneIndex(self, index):
        '''
                        根据用例编号获取对应的可用手机
        @param index: 用例编号
        @param d_list: 手机信息列表长度
        '''
        try:
            # 直接取模，获取对应手机
            hash_rslt = (index) % self._devices_list.t_size()
            dvc_info = None
            i = 0
            while True:
                # 如果手机状态为1说明可用，直接返回列表中该手机对应的索引
                dvc_info = self._devices_list.getDevcByIndex(hash_rslt)
                if dvc_info:
                    return dvc_info
                # 第一次取模后获取的手机不可用时判读下一个手机是否可用
                else:
                    i = i + 1
                    hash_rslt = (index + i) % self._devices_list.t_size()
        except:
            return None
        
    def _insertResultQueue(self, result_queue):
        '''
        先将结果保存在队列中，然后通知结果处理线程已经生成了结果
        @param test_result:测试结果，测试成功返回True，失败返回False
        @param test_case:测试用例
        @param devc_info:测试手机信息
        @param case_result:测试结果，执行测试用例返回的结果
        @param install_apk_result:安装apk返回的信息，包含安装、卸载时间信息
        '''
        self._result_queue.put(result_queue)
        self._result_cond.acquire()
        self._result_cond.notify()
        self._result_cond.release()
        
    def updateDevcAndInsertQueue(self, serial, state, work_queue, result_queue): 
        if not self._devices_list.setStateBySerial(serial, state):
            self._work_queue.put(work_queue)
        else:
            self._insertResultQueue(result_queue)
        
    def run(self):
        '''
                        线程入口函数
        '''
        while True:
            # 如果守护线程标志位为True，说明检测到异常， 则不继续执行
            if self._dvc_event.is_set():
                break
            try:
                args, kwds = self._work_queue.get(timeout=self.__class__.queue_timeout)
                test_case = args[0]
                devc_info = self.getPhoneIndex(args[1])
                if not devc_info:
                    break
                serial = devc_info.serial

                # （手机第一次连接）或者（非第一次并且配置文件说明需要每次都安装apk）
                inst_apk_rslt = None
                if devc_info.first_install or ((not devc_info.first_install) and self._install_apk):
                    is_success, inst_apk_rslt = devc_info.installApk(self._apk_path, self._uni_path)
                    if not is_success:
                        self.updateDevcAndInsertQueue(serial, 1, (args, kwds), \
                                                      (False, test_case, devc_info, 'install apk failed!', None, None))
                        continue
                    if devc_info.first_install:
                        self._devices_list.updateDevcFirstInst(devc_info)
                    # 初次执行时需要进行的操作
                    if self.prepareWorkForDevice != None:
                        if not self.prepareWorkForDevice(serial):
                            self.updateDevcAndInsertQueue(serial, 1, (args, kwds), \
                                                          (False, test_case, devc_info, 'prepare work failed!', None, None))
                            continue

                # 执行测试用例前需要执行的操作
                # 预处理，由测试人员实现
                if self.prepareWorkForCase != None:
                    self.prepareWorkForCase(serial)

                # 执行测试过程，具体过程由测试人员实现
                start_time = time.time()
                case_rslt = self.runTestCase(test_case, serial)
                exec_time = time.time() - start_time
                
                # 再次判断标志位是否为True，以防在执行过程中手机失联，这种情况下的结果不需要插入队列
                if self._dvc_event.is_set():
                    break
                # 为防止手机失去连接，此时用手机序列号更新手机状态
                time.sleep(0.5)  # 有待改进
                self.updateDevcAndInsertQueue(serial, 1, (args, kwds), \
                                              (True, test_case, devc_info, case_rslt, inst_apk_rslt, exec_time))

            except Queue.Empty:
                break
            except:
                self._devices_list.setStateBySerial(serial, 1)
                continue

if __name__ == '__main__':
    pass
