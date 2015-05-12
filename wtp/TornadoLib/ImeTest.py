#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-10 09:07'

import tornado.web
import tornado.websocket
import tornado.ioloop
import random
import time


class ImeTestHandler(tornado.web.RequestHandler):
    # def get(self):
    #     import time
    #     for i in range(10):
    #         self.write('this is ime test')
    #         time.sleep(1)
    @tornado.web.asynchronous
    def get(self):
        self.get_data(callback=self.on_finish)

    def get_data(self, callback):
        if self.request.connection.stream.closed():
            return

        num = random.randint(1, 100)
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time()+3,
            lambda: callback(num)
        )

    def on_finish(self, data):
        self.write("Server says: %d" % data)
        self.finish()
