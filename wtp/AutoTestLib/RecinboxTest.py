#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-10 09:08'

import tornado.web


class RecinboxTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('this is recinbox test')
