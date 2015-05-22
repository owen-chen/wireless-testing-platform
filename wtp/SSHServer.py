#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sqxu'
__date__ = '2015-03-19 16:03'
"""
该类实现从文件服务器中下载文件到本机指定目录下
"""

import os

import paramiko


class SSHServer():
    """
    从文件服务器下载相关文档到本地临时文件夹
    """
    def __init__(self, target_host, target_port, user_name, pass_word):

        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=target_host, port=target_port, username=user_name, password=pass_word)
        self._sftp = self._ssh.open_sftp()

    def getFileFromDocumentServer(self, remote_document, local_path):
        """
        @:param remote_document:需要从文件服务器中下载到本地的文件夹
        @:param local_path: 下载到本地的地址
        """
        sub_remote_files = self._sftp.listdir(remote_document)
        for sub_file in sub_remote_files:
            target_file = remote_document + '/' + sub_file
            stdin, stdout, stderr = self._ssh.exec_command('cd %s' % target_file)
            if 'Not a directory' in stderr.read():
                if not os.path.isdir(local_path):
                    os.makedirs(local_path)
                self._sftp.get(target_file, local_path + '/' + sub_file)
            else:
                self.getFileFromDocumentServer(remote_document + '/' + sub_file, local_path + '/' + sub_file)

    def __del__(self):
        self._sftp.close()
        self._ssh.close()

if __name__ == '__main__':
    import time
    s = time.time()
    SSHServer('172.16.95.14', 22, 'cis', 'cis')
    print time.time() - s
