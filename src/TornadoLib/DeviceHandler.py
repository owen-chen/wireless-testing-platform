#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-05 17:02'

"""
该模块中获取手机状态信息
"""

import tornado.web

from JsonText import JsonText
from XmlText import XmlTest
from AutoTestLib.DevicesManage import DevicesManage


class DeviceHandler(tornado.web.RequestHandler):
    def get(self):
        devc_mgr = DevicesManage()
        available_devices_list, unavailable_devices_list = devc_mgr.getDevicesList()
        api_type = self.get_argument('api', 'json')
        pretty_value = self.get_argument('pretty', 'false')
        if api_type == 'json':
            json_text = JsonText(available_devices_list, unavailable_devices_list, pretty_value)
            self.render('result.html', result_text=json_text.get_json_result())
        else:
            xml_text = XmlTest(available_devices_list, unavailable_devices_list)
            self.render('result.html.', result_text=xml_text.get_xml_text())



