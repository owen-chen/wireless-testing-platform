# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import sys

import MySQLdb

from Singleton import singleton


@singleton
class TestcaseResultDao:
    def __init__(self):
        self.db = MySQLdb.connect(
            host='172.16.95.14',
            user='root',
            passwd='root',
            db='jenkins',
            port=3306,
            charset='utf8'
        )
    
    def insert(self, testcaseResult):
        cursor = self.db.cursor()
        try:
            sql = "INSERT INTO testcase_result(testcase_name, uuid, parent_uuid, device_info) VALUES (%s, %s, %s, %s)"
            sys.stderr.write("parentUuid: %s" % (testcaseResult.parentUuid))
            cursor.execute(sql, (testcaseResult.testcaseName, testcaseResult.uuid, testcaseResult.parentUuid, testcaseResult.deviceInfo))
        except Exception, e:
            sys.stderr.write(str(e))
            self.db.rollback()
        
    def update(self, testcaseResult, resultList=[]):
        for result in resultList:
            testcaseResult.result += result
        
        cursor = self.db.cursor()
        try:
            sql = "UPDATE testcase_result SET result = %s, isEnd = %s, isSuccess = %s WHERE testcase_name = %s AND uuid = %s"
            cursor.execute(sql, (testcaseResult.result, testcaseResult.isEnd, testcaseResult.isSuccess, testcaseResult.testcaseName, testcaseResult.uuid))
        except Exception, e:
            sys.stderr.write(str(e))
            self.db.rollback()
            
    def retrieveAllInOneJob(self, parentUuid):
        cursor = self.db.cursor()
        sql = "SELECT result, device_info, isSuccess, testcase_name FROM testcase_result WHERE parent_uuid = %s AND isEnd = 1"
        cursor.execute(sql, (parentUuid,))
        return cursor.fetchall()
        
    def retrieveLastOne(self, testcaseName):
        cursor = self.db.cursor()
        sql = "SELECT result, isEnd, isSuccess FROM testcase_result WHERE testcase_name = %s ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql, (testcaseName,))
        return cursor.fetchone()
            
    def retrieve(self, testcaseName, uuid):
        cursor = self.db.cursor()
        sql = "SELECT result, isEnd, isSuccess FROM testcase_result WHERE testcase_name = %s AND uuid = %s LIMIT 1"
        cursor.execute(sql, (testcaseName, uuid))
        return cursor.fetchone()
