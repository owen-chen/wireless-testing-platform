# -*- coding: utf-8 -*-
'''
Created on Jun 2, 2015

@author: chenchen
'''
import tornado.web


class TestcaseResultListHtmlController(tornado.web.RequestHandler):
    def get(self):
        self.render('resultList.html', uuid=self.get_argument('uuid', ''))
        