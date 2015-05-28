# -*- coding: utf-8 -*-
'''
    结果展示线程，该线程将工作线程中产生的结果队列的信息抓取出来并将其展示。该线程随主线程的结束而结束
    @since: 2014-12-26
    @author: sqxu
    @author: chenchen9
'''

import Queue
from threading import Thread

from CommonLib import ciWrite


class AnalysisResultThread(Thread):
    ''' constructor '''
    def __init__(self, rslt_queue, result_path, no_dvc_ent, rslt_cond, getRsltFunc):
        """
        @param _result_queue: 保存结果的队列
        @param _result_path: 保存结果的路径
        @param _dvc_event: 是否有手机连接的标志位
        """
        super(AnalysisResultThread, self).__init__()
        self.setDaemon(True)
        self.setName('AnalysisResultThread')
        self._result_queue = rslt_queue
        self._result_path = result_path
        self._dvc_event = no_dvc_ent
        self._result_cond = rslt_cond
        self.getResultFunc = getRsltFunc


    # def _writeLog(self, log_path):
    #     """
    #
    #     """
    #    rslt_dir = log_path + '\\' + result[2].product
    #    rslt_file = rslt_dir + '\\' + result[2].serial + '.txt'
    #    if not os.path.isdir(rslt_dir):
    #        os.makedirs(rslt_dir)
    #    fp = open(rslt_file, 'a+')

    def _printAndLog(self, result_dict, devc_info, case_name, inst_info, exec_time):
        ciWrite(case_name)
        if inst_info != None:
            if 'uni_time' in inst_info.keys():
                ciWrite(case_name, 'UNINSTALL_ELAPSED_TIME##%.2f' % inst_info['uni_time'])
                ciWrite(case_name, 'UNINSTALL_RESULT##success')
            ciWrite(case_name, 'INSTALL_ELAPSED_TIME##%.2f' % inst_info['ins_time'])
            ciWrite(case_name, 'INSTALL_RESULT##success')

        ciWrite(case_name, '%s' % result_dict['result'])
        ciWrite(case_name, 'EXECUTE_ELAPSED_TIME##%.2f' % exec_time)
        if result_dict['result'] != 'success':
            ciWrite(case_name, 'DEVICE##%s，%s，%s，%s' % (devc_info.product, devc_info.resolution, \
                                                            devc_info.edition, devc_info.serial))
            if len(result_dict['msg']) > 0:
                for line in result_dict['msg']:
                    ciWrite(case_name, '%s' % line.decode('utf-8').encode('gbk'))

    def analysisResult(self, result):  
        """
                        对结果进行解析，以更直观的方式显示
        @param result: 从结果队列中取到的结果，数据以表列的形式存储
        """
        
        test_reuslt, test_case, devc_info, case_result, inst_info, exec_time = result
        case_name = getCaseName(test_case)
        if test_reuslt:
            self._printAndLog(self.getResultFunc(case_result, case_name), devc_info, case_name, inst_info, exec_time)
        else:
            self._printErrorInfo(case_name, case_result, devc_info)
            
    def _printErrorInfo(self, case_name, case_result, devc_info):
        ciWrite(case_name, '')
        ciWrite(case_name, 'failed')
        ciWrite(case_name, '$DEVICE##%s，%s，%s，%s' % (devc_info.product, devc_info.resolution, \
                                                        devc_info.edition, devc_info.serial))
        ciWrite(case_name, case_result)
    
    def run(self):
        """
        队列中取数据，然后对数据进行分析处理，包括文档记录和控制台打印
        """
        while True:
            if self._dvc_event.is_set():
                    break
            try:
                self._result_cond.acquire()
                if self._result_queue.qsize() <= 0:
                    self._result_cond.wait()
                self._result_cond.release()  
                
                result = self._result_queue.get()
                if self._dvc_event.is_set():
                    break
                self.analysisResult(result)
            except Queue.Empty:
                break
            except :
                pass
