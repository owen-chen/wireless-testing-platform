#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-19 10:06'

"""
根据手机信息列表生成对应的xml
"""

from xml.dom.minidom import Document

class XmlTest(Document):
    def __init__(self, available_devices_list, unavailable_devices_list):
        Document.__init__(self)
        self._available_devices_list = available_devices_list
        self._unavailable_devices_list = unavailable_devices_list

    def __add_sub_node(self, node, sub_node, sub_string):
        """
        根据传入的参数生成子节点
        @:param node：父节点
        @:param sub_node: 子节点名字
        @:param sub_string：子节点的文字描述
        """
        sub_node = self.createElement(sub_node)
        sub_node_text = self.createTextNode(sub_string)
        sub_node.appendChild(sub_node_text)
        node.appendChild(sub_node)

    def get_xml_text(self):
        self.tag = self.createElement('devices_info')
        self.appendChild(self.tag)
        self.tag.setAttribute('count', str(len(self._available_devices_list) + len(self._unavailable_devices_list)))

        self.sub_available_tag = self.createElement('available_devices')
        self.sub_available_tag.setAttribute('count', str(len(self._available_devices_list)))
        self.tag.appendChild(self.sub_available_tag)
        if len(self._available_devices_list) > 0:
            for avail_devc in self._available_devices_list:
                devc_tag = self.createElement('device')
                devc_tag.setAttribute('serial', avail_devc.serial)
                self.__add_sub_node(devc_tag, 'product', avail_devc.product)
                self.__add_sub_node(devc_tag, 'memory_state', avail_devc.memory_size + '/' + avail_devc.memory_free)
                self.__add_sub_node(devc_tag, 'edition', avail_devc.edition)
                self.__add_sub_node(devc_tag, 'sim_state', str(avail_devc.sim_state))
                self.__add_sub_node(devc_tag, 'resolution', avail_devc.resolution)
                self.sub_available_tag.appendChild(devc_tag)

        self.sub_uavailable_tag = self.createElement('uavailable_devices')
        self.sub_uavailable_tag.setAttribute('count', str(len(self._unavailable_devices_list)))
        self.tag.appendChild(self.sub_uavailable_tag)
        if len(self._unavailable_devices_list) > 0:
            for uavail_devc in self._unavailable_devices_list:
                devc_tag = self.createElement('device')
                devc_tag.setAttribute('serial', uavail_devc[0])
                self.__add_sub_node(devc_tag, 'state', str(uavail_devc[1]))
                self.sub_uavailable_tag.appendChild(devc_tag)

        return self.toprettyxml()

if __name__ == '__main__':
    pass
