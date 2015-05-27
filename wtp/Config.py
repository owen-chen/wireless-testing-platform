# -*- coding: utf8 -*-
"""
Created on 2014/12/5
配置文件读取类
@author: sqxu
@author: chenchen9
"""
import os
import sys
from CommonLib import ciWrite


class Config():
    '''配置文件处理类，主要完成从配置文件中获取关键信息，以及其他一些文件操作'''

    def __init__(self, file_name, apk_path):
        '''
        @param file_name: 配置文件路径
        @param apk_path: apk路径，支持配置文件方式和参数传入方式，优先选择参数传入方式
        @param apk_signed: 是否需要签名
        @param _test_case_file: 测试用例文件路径
        @param _is_install_apk: 是否自动安装apk
        @param _result_dir: 测试结果文件
        @param uni_apk_path: 需要卸载的apk路径
        '''
        self._cfg_name = file_name
        if not os.path.isfile(self._cfg_name):
            ciWrite('ERROR', 'can\'t find %s file' % self._cfg_name)
            sys.exit()
            
        self.apk_path = apk_path
        self.test_case_file = None
        self.debug_store = None
        self.uni_apk_path = None
        self.thread_time_out = 120
        self.thread_numb = 10
        self.apk_signed = 0
        self.install_apk = 0

        self.test_py_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/'
        
        self.cfg_dict = self.parseFile()
        self._initParams()
        
    def _initParams(self):
        dict_key = self.cfg_dict.keys()
        if self.apk_path == None:
            if ('apk_path' not in dict_key) or (not self.cfg_dict['apk_path']):
                ciWrite('ERROR', 'apk path is NULL')
                sys.exit()
            else:
                self.apk_path = self.test_py_path + self.cfg_dict['apk_path']
        
        if ('uni_apk_path' in dict_key) and (self.cfg_dict['uni_apk_path']):
            self.uni_apk_path = self.cfg_dict['uni_apk_path']
            
        if ('test_case_file' in dict_key) and (self.cfg_dict['test_case_file']):
            self.test_case_file = self.test_py_path + self.cfg_dict['test_case_file']
            
        if ('debug_key_store' in dict_key) and (self.cfg_dict['debug_key_store']):
            self.debug_store = self.test_py_path + self.cfg_dict['debug_key_store']
            
        if ('apk_signed' in dict_key) and (self.cfg_dict['apk_signed']):
            self.apk_signed  = int(self.cfg_dict['apk_signed'])
            
        if ('thread_time_out' in dict_key) and (self.cfg_dict['thread_time_out']):
            self.thread_time_out = float(self.cfg_dict['thread_time_out'])
            
        if ('thread_count' in dict_key) and (self.cfg_dict['thread_count']):
            self.thread_numb = int(self.cfg_dict['thread_count'])
            
        if ('install_apk' in dict_key) and (self.cfg_dict['install_apk']):
            self.install_apk = int(self.cfg_dict['install_apk'])
            
    def parseFile(self):
        '''
                        获取配置文件中的信息，并将信息保存在字典中
        '''
        cfg_dict = {}
        fp = open(self._cfg_name, 'r')
        
        lines = [line.strip() for line in fp.readlines() if line.strip() and not line.startswith('#')]
        fp.close()
        for line in lines:
            line = line.strip()
            if line.find('=') >= 0:
                line_list = line.split('=')
                key, value = line_list[0].strip(), line_list[1].strip()
                if value:
                    cfg_dict[key] = value
                else:
                    cfg_dict[key] = ''
        
        return cfg_dict


# --------------------测试部分--------------------------
if __name__ == "__main__":
    fm = Config("config.txt")
    print fm.cfg_dict
