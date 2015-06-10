# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import uuid


class TestcaseResult:
    def __init__(self):
        self.deviceInfo = None
        self.parentUuid = None
        self.uuid = uuid.uuid4()
        self.testcaseName = None
        self.result = ''
        self.isEnd = 0
        self.isSuccess = 0
        
    def toDict(self):
        testcase_result_dict = {}
        testcase_result_dict['deviceInfo'] = self.deviceInfo
        testcase_result_dict['parentUuid'] = self.parentUuid
        testcase_result_dict['uuid'] = self.uuid
        testcase_result_dict['testcaseName'] = self.testcaseName
        testcase_result_dict['result'] = self.result
        testcase_result_dict['isEnd'] = self.isEnd
        testcase_result_dict['isSuccess'] = self.isSuccess
        return testcase_result_dict
