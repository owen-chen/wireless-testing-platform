# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import json

import tornado.web

from TestcaseResult import TestcaseResult
from TestcaseResultDao import TestcaseResultDao


class TestcaseResultListController(tornado.web.RequestHandler):
    ''' 查看测试用例结果 '''
    def get(self):
        uuid = self.get_argument('uuid')
        
        if not uuid:
            raise Exception
        
        resultsets = TestcaseResultDao().retrieveAllInOneJob(uuid)
        if not resultsets:
            self.write({"successful": False})
        else:
            testcaseResultListDict = {'testcase_result_list' : []}
            for resultset in resultsets:
                testcaseResult = TestcaseResult()
                testcaseResult.result = '<br />'.join(resultset[0].splitlines())
                testcaseResult.deviceInfo = resultset[1]
                testcaseResult.isSuccess = resultset[2]
                testcaseResult.testcaseName = resultset[3]
                
                testcaseResultListDict['testcase_result_list'].append(testcaseResult.toDict())

            self.write({"successful": True, 'testcaseResultArray': json.dumps(testcaseResultListDict,  indent=4)})        
