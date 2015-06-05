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
        print apkpath
        exist = os.path.isfile(apkpath)
        if not exist:
            raise Exception
        
        ''' 2. 读取测试用例配置 '''
        projectname = self.get_argument('projectname')
        tempPath = projectname.replace("-", "/")

        while True:
            testcasePath = "%s/%s/testcase.xml" % (Configuration().dicts['testcase']['testcaseServer'], tempPath)
            exist = os.path.isfile(testcasePath)
            if exist:
                break
            
            if (tempPath.find('/') == -1 and tempPath.find('_') == -1) or not tempPath:
                raise Exception
            if tempPath.find('_') != -1:
                tempPath = tempPath[:tempPath.rindex('_')]
            else:
                tempPath = tempPath[:tempPath.rindex('/')]
            
        ''' 3. 解析xml，反序列化 '''
        testcaseList = TestcaseReader(testcasePath, apkpath).testcaseList;
            
        ''' 4. 循环读取命令，在线程池中运行 '''
        for testcase in testcaseList:
            TestcaseManager().process(testcase)
            
        self.write({'success': True})
