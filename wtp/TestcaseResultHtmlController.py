# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import tornado.web


class TestcaseResultHtmlController(tornado.web.RequestHandler):
    def get(self):
        self.render('result.html', name=self.get_argument('name'), uuid=self.get_argument('uuid', ''))
        