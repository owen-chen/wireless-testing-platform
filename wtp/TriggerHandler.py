# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen9
'''
import subprocess

import tornado.web

class TriggerHandler(tornado.web.RequestHandler):
    def get(self):
        projectname = self.get_argument('projectname')
        
        
        
        
        sub_process = subprocess.Popen('python ../lingxitest.py', stderr=subprocess.PIPE)
        std_err = sub_process.stderr.readline()
        while sub_process.poll() == None and std_err:
            self.write(std_err)
            self.flush()
            std_err = sub_process.stderr.readline()
