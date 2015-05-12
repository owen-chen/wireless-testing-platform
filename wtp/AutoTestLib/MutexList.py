# -*- coding: utf-8 -*-
#MutexList.py
'''
Created on 2014年12月23日
@author: sqxu
'''

import threading

class MutexList():
    '''
            对列表进行封装，保证其线程安全
    '''
    def __init__(self, d_list):
        '''
        @param _deviceslist: 信息列表 
        @param _mutex: 保证列表线程安全
        '''
        self._devices_list = []
        self._mutex = threading.Lock()
        self._initList(d_list)
        
    def _initList(self, d_list):
        '''
                        增加列表元素
        @param d_list: 
        '''
        try:
            self._mutex.acquire()
            self._devices_list = d_list
            self._mutex.release()
        except:
            self._mutex.release()
            pass

    def t_size(self):
        '''
                        返回列表大小
        '''
        try:
            self._mutex.acquire()
            n = len(self._devices_list)
            self._mutex.release()
            return n
        except:
            self._mutex.release()
            pass
    
    def getState(self, index):
        '''
                        根据index对应设备的状态，即‘state’
        @param index:
        @param str:
        '''
        try:
            self._mutex.acquire()
            state = self._devices_list[index].getState()
            self._mutex.release()
            return state
        except:
            self._mutex.release()
            pass
    
    def setState(self, index, state):
        '''
                        根据index和str返回列表中的值
        @param index:
        @param state:
        '''
        try:
            self._mutex.acquire()
            self._devices_list[index].setState(state)
            self._mutex.release()
        except:
            self._mutex.release()
            pass
    
    def getELement(self, index):
        '''
        根据索引获取列表中对应的手机信息
        @param index: 索引号
        '''
        try:
            self._mutex.acquire()
            info = self._devices_list[index]
            self._mutex.release()
            return info
        except:
            self._mutex.release()
            pass
    
    def setStateBySerial(self, serial, value):
        '''
        根据手机序列号更新手机列表中对应的手机状态，默认情况下是可以根据序列号进行修改的，如果出现异常或者没有找到对应手机信息，说明该手机已经失去连接
        @param serial: 序列号
        @param value: 更新状态值
        '''
        self._mutex.acquire()
        flag = False
        try:
            for dvc in self._devices_list:
                if dvc.serial == serial:
                    dvc.setState(value)
                    flag = True
        except Exception,e:
            flag = False
        finally:
            self._mutex.release()
        return flag
        
    def updateListByList(self, devc_list):
        '''
                        根据devc_list检索信息列表，对信息列表做出相应修改
        @param devc_list: 新获取的手机信息列表
        '''
        try:
            self._mutex.acquire()
            #---------------说明新添加手机，通知安装apk线程进行处理
            temp = []
            for devc in self._devices_list:
                flag = False
                for cur_dec in devc_list:
                    if devc.serial == cur_dec.serial:
                        flag = True
                        break
                if not flag:
                    temp.append(devc)
                    
            #--------删除已经失去连接的手机信息
            for dvc in temp:
                self._devices_list.remove(dvc)
                
            #-------------遍历新列表，如果手机列表中已经存在不做处理，如果没有则添加至手机列表中，但状态为0，为安装apk
            #-------------add_dvc标志位，为True说明有新手机加入连接
            for cur_dvc in devc_list:
                flag = False
                for last_dvc in self._devices_list:
                    if cur_dvc.serial == last_dvc.serial:
                        flag = True
                        break
                if not flag:
                    self._devices_list.append(cur_dvc)
                    
            self._mutex.release()
        except:
            self._mutex.release()
            pass
        
    def getUinstallDevices(self):
        '''
        返回所有未安装apk的手机，即手机状态为0的所有的手机信息
        '''
        try:
            self._mutex.acquire()
            ret_list = []
            for dvc in self._devices_list:
                if dvc.getState() == 0:
                    ret_list.append(dvc)
            self._mutex.release()
            
            return ret_list
        except:
            self._mutex.release()
            pass
    
    def clearList(self):
        '''
        清除手机信息列表
        '''
        try:
            self._mutex.acquire()
            self._devices_list = []
            self._mutex.release()
        except:
            self._mutex.release()
            pass
        
    def delElement(self, devc_info):
        '''
        删除对应的元素
        @param devc_info:
        '''
        try:
            self._mutex.acquire()
            if devc_info in self._devices_list:
                self._devices_list.remove(devc_info)
            self._mutex.release()
        except:
            self._mutex.release()
            pass
        
    def getDevcByIndex(self, index):
        '''
        根据索引号获取手机信息
        @param index:
        '''
        devc = None
        try:
            self._mutex.acquire()
            if self._devices_list[index].getState() == 1:
                self._devices_list[index].setState(-1)
                devc = self._devices_list[index]
        except:
            pass
        finally:
            self._mutex.release()
        return devc
    
    def updateDevcFirstInst(self, devc_info):
        '''
        更新手机信息，第一次执行测试用例后，将对应手机的信息更改为False，表示已经执行过用例了。
        @param devc_info:
        '''
        try:
            self._mutex.acquire()
            for devc in self._devices_list:
                if devc == devc_info:
                    devc.updateFirstInstallInfo()
            self._mutex.release()
        except:
            self._mutex.release()
            pass

#------------------测试部分，验证该类线程安全性---------------------       
if __name__ == '__main__':
    pass

    
