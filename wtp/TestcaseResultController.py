# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import tornado.web

from TestcaseResultDao import TestcaseResultDao


class TestcaseResultController(tornado.web.RequestHandler):
    ''' 查看测试用例结果 '''
    def get(self):
        uuid = self.get_argument('uuid', None)
        name = self.get_argument('name')
        line = int(self.get_argument('line', 0))
        
        if not name:
            raise Exception
        
        if uuid:
            results = TestcaseResultDao().retrieve(name, uuid)
        else:
            results = TestcaseResultDao().retrieveLastOne(name)
            
        if not results:
            self.write({"successful": False})
        else:
            result = ''
            if results[0]:
                lines = results[0].splitlines()
                if len(lines) > line:
                    result = '<br />'.join(lines[line + 1:])
    
            self.write({"successful": True, "result": result, "isEnd": results[1], "isSuccess": results[2], "line": len(lines)})        