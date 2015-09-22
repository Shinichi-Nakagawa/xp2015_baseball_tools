#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from service.storage import Storage

class StorageUploader(object):

    def __init__(self, config_file='./config/app.ini'):
        self.storage_service = Storage(config_file)

    def upload_files(self, input_dir, extension, now_time):
        """
        ファイル転送
        :param input_dir: input_dir
        :param extension: ext
        :param now_time: timestamp(string)
        :return: None
        """
        self.storage_service.upload_files(input_dir, extension, now_time)
