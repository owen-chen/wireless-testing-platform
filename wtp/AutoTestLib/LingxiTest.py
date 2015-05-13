#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-09 10:50'

import subprocess

import tornado.web


class LingxiTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('this is lingxi test\n')

        sub_process = subprocess.Popen('python ../lingxitest.py', stderr=subprocess.PIPE)
        std_err = sub_process.stderr.readline()
        while sub_process.poll() == None and std_err:
            self.write(std_err)
            self.flush()
            std_err = sub_process.stderr.readline()


if __name__ == '__main__':
    sub_process = subprocess.Popen('python ../lingxitest.py', stderr=subprocess.PIPE)
    std_out = sub_process.stderr.readline()
    while sub_process.poll() == None and std_out:
        print std_out
        std_out = sub_process.stderr.readline()
