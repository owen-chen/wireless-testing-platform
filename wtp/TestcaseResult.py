# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import uuid


class TestcaseResult:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.testcaseName = None
        self.result = ''
        self.isEnd = 0
        self.isSuccess = 0
