# -*- coding: utf8 -*-
"""
Created on Dec 5, 2014

@author: chenchen9
"""
import lazyxml

from Singleton import singleton


@singleton
class Configuration():
    '''
        配置文件处理类，主要完成从配置文件中获取关键信息，以及其他一些文件操作
        @param file_name: 配置文件路径
    '''
    def __init__(self):
        xml = open("config.xml").read()
        self.dicts = lazyxml.loads(xml, strip=False)