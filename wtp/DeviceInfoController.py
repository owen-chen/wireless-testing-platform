# -*- coding: utf-8 -*-
'''
Created on May 15, 2015

@author: chenchen9
@author: sqxu
'''

import json
from json.encoder import JSONEncoder

import jsonpickle
import lazyxml
import tornado.web

from DeviceManager import DeviceManager


class DeviceInfoController(tornado.web.RequestHandler):
    def get(self):
        deviceInfoList = DeviceManager().findDeviceList()
        dict = deviceInfoList.toDict()
        print dict
        api_type = self.get_argument('api', 'json')
        pretty = self.get_argument('pretty').lower() == 'true'
        
        if api_type == 'json':
            if pretty:
                devices_info = json.dumps(dict, indent=4)
            else:
                devices_info = json.dumps(dict)
        elif api_type == 'xml':
            if pretty:
                devices_info = lazyxml.dumps(dict, root='device_list', cdata=False, indent='    ')
            else:
                devices_info = lazyxml.dumps(dict, root='device_list', cdata=False)
        else:
            raise Exception('unsupported argument: ' + api_type) 
        
        self.render('result.html', result_text=devices_info)



