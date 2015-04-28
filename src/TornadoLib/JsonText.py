#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-19 10:06'

"""
根据手机信息列表生成json串，在页面上展示的结果根据传入的pretty值进行区分
"""

import json


class JsonText():
    def __init__(self, available_devices_list, unavailable_devices_list, prty_value):
        self._available_devices_list = available_devices_list
        self._unavailable_devices_list = unavailable_devices_list
        self._pretty_value = prty_value

    def get_json_result(self):
        devices_state_dict = {}
        available_list = []
        unavailable_list = []

        for device_info in self._available_devices_list:
            devc_info = {}
            devc_info['serial'] = device_info.serial
            devc_info['product'] = device_info.product
            devc_info['resolution'] = device_info.resolution
            devc_info['edition'] = device_info.edition
            devc_info['memory_state'] = device_info.memory_size + '/' + device_info.memory_free
            devc_info['sim_state'] = device_info.sim_state
            available_list.append(devc_info)
        devices_state_dict['available_devices'] = available_list

        for device_info in self._unavailable_devices_list:
            devc_info = {}
            devc_info['serial'] = device_info[0]
            devc_info['state'] = device_info[1]
            unavailable_list.append(devc_info)
        devices_state_dict['unavailable_devices'] = unavailable_list

        devices_count = len(available_list) + len(unavailable_list)
        devices_state_dict['devices_count'] = devices_count

        if self._pretty_value == 'false':
            return str(devices_state_dict).replace(' ', '')
        else:
            return json.dumps(devices_state_dict, indent=1)


if __name__ == "__main__":
    pass
