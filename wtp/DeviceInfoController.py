# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen9
'''

import json

import lazyxml
import tornado.web

from DeviceManager import DeviceManager


class DeviceInfoController(tornado.web.RequestHandler):
    def get(self):
        dicts = DeviceManager().getDeviceInfoList().toDict()
        
        api_type = self.get_argument('api', 'json')
        pretty = self.get_argument('pretty', 'false').lower() == 'true'
        if api_type == 'json':
            if pretty:
                devices_info = json.dumps(dicts, indent=4)
            else:
                devices_info = json.dumps(dicts)
        elif api_type == 'xml':
            if pretty:
                devices_info = lazyxml.dumps(dicts, root='device_list', cdata=False, indent='    ')
            else:
                devices_info = lazyxml.dumps(dicts, root='device_list', cdata=False)
        else:
            raise Exception('unsupported argument: ' + api_type) 
        
        self.write(devices_info)