# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen
'''

import os

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.options
import tornado.web

from Configuration import Configuration
from DeviceInfoController import DeviceInfoController
from DeviceManager import DeviceManager
from ProcessController import ProcessController
from TestcaseResultController import TestcaseResultController
from TestcaseResultHtmlController import TestcaseResultHtmlController
from TestcaseResultListController import TestcaseResultListController
from TestcaseResultListHtmlController import TestcaseResultListHtmlController
from ThreadPoolManager import ThreadPoolManager


class TornadoProcessor:
    def __init__(self):
        Configuration()
        DeviceManager()
        ThreadPoolManager()

        define('port', 80, None, int)

    def run(self):
        settings = {'static_path': os.path.join(os.path.dirname(__file__), '')}
        
        tornado.options.parse_command_line()
        application = tornado.web.Application(handlers=[(r'/(favicon\.png)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                                        (r'/(jquery-1\.10\.2\.min\.js)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                                        (r'/', DeviceInfoController),
                                                        (r'/devices', DeviceInfoController),
                                                        (r'/process', ProcessController),
                                                        (r'/result', TestcaseResultController),
                                                        (r'/resultList', TestcaseResultListController),
                                                        (r'/resultHtml', TestcaseResultHtmlController),
                                                        (r'/resultListHtml', TestcaseResultListHtmlController)
                                                        ], **settings)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
