# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen
'''
import os

import tornado.web

from Configuration import Configuration
from TestcaseManager import TestcaseManager
from TestcaseReader import TestcaseReader


class ProcessController(tornado.web.RequestHandler):
    ''' 执行测试用例 '''
    def get(self):
        ''' 1. 确定交付包位置 '''
        apkpath = "%s/%s" % (Configuration().dicts['testcase']['packageServer'], self.get_argument('apkpath'))
        exist = os.path.isfile(apkpath)
        if not exist:
            raise Exception
        
        ''' 3. 解析xml，反序列化 '''
        testcaseReader = TestcaseReader(apkpath, self.get_argument('projectname'));
            
        ''' 4. 循环读取命令，在线程池中运行 '''
        for testcase in testcaseReader.testcaseList:
            TestcaseManager().process(testcase)
            
        self.write({'success': True, 'uuid': testcaseReader.uuid})
