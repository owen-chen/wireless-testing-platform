# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen
'''

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.options
import tornado.web

from Configuration import Configuration
from DeviceInfoController import DeviceInfoController
from DeviceManager import DeviceManager
from ProcessHandler import ProcessHandler
from ThreadPoolManager import ThreadPoolManager


class TornadoProcessor:
    def __init__(self):
        Configuration()
        DeviceManager()
        ThreadPoolManager()

        define('port', 80, None, int)

    def run(self):
        tornado.options.parse_command_line()
        application = tornado.web.Application(handlers=[(r'/', DeviceInfoController),
                                                        (r'/devices', DeviceInfoController),
                                                        (r'/process', ProcessHandler)
                                                        ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
