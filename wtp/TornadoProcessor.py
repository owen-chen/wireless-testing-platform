# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen9
@author: sqxu
'''

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.options
import tornado.web

from DeviceInfoController import DeviceInfoController
from ImeTest import ImeTestHandler
from LingxiTest import LingxiTestHandler
from RecinboxTest import RecinboxTestHandler
from TriggerHandler import TriggerHandler


class TornadoProcessor:
    def __init__(self):
        define('port', 9000, None, int)

    def run(self):
        tornado.options.parse_command_line()
        application = tornado.web.Application(handlers=[(r'/devices', DeviceInfoController),
                                                        (r'/trigger', TriggerHandler),
                                                        (r'/lingxi', LingxiTestHandler),
                                                        (r'/ime', ImeTestHandler),
                                                        (r'/recinbox', RecinboxTestHandler)
                                                        ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
