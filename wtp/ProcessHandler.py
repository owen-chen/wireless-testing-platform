# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen9
'''
import os

import tornado.web

from TestcaseManager import TestcaseManager
from TestcaseReader import TestcaseReader


class ProcessHandler(tornado.web.RequestHandler):
    ''' 执行测试用例 '''
    def get(self):
        ''' 1. 确定交付包位置 '''
        apkpath = "%s/%s" % ('/disk1/PackageServer', self.get_argument('apkpath'))
        exist = os.path.isfile(apkpath)
        if not exist:
            raise Exception
        
        ''' 2. 读取测试用例配置 '''
        projectname = self.get_argument('projectname')
        tempPath = projectname.replace("-", "/")

        while True:
            testcasePath = "%s/%s/testcase.xml" % ('/disk1/CIS/shared', tempPath)
            exist = os.path.isfile(testcasePath)
            if exist:
                break
            
            if (tempPath.index('/') == -1 and tempPath.index('_') == -1) or not tempPath:
                raise Exception
            if tempPath.index('_') != -1:
                tempPath = tempPath[:tempPath.rindex('_')]
            else:
                tempPath = tempPath[:tempPath.rindex('/')]
            
        ''' 3. 解析xml，反序列化 '''
        testcaseList = TestcaseReader(testcasePath, apkpath).testcaseList;
            
        ''' 4. 循环读取命令，在线程池中运行 '''
        for testcase in testcaseList:
            TestcaseManager().process(testcase)
