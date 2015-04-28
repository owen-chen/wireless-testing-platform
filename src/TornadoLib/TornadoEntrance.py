#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-05 16:57'

"""
启动web服务入口
"""

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options

from DeviceHandler import DeviceHandler
from LingxiTest import LingxiTestHandler
from ImeTest import ImeTestHandler
from RecinboxTest import RecinboxTestHandler


define('port', default=8000, help='run on the given port', type=int)  # 处理命令行中的参数


def main():
    tornado.options.parse_command_line()  # 使用options来解析命令行
    application = tornado.web.Application(handlers=[(r'/devices', DeviceHandler),
                                                    (r'/lingxi', LingxiTestHandler),
                                                    (r'/ime', ImeTestHandler),
                                                    (r'/recinbox', RecinboxTestHandler)
                                                    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
