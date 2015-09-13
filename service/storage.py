#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from configparser import ConfigParser
from boto3.session import Session
import glob
import os

class Storage(object):

    def __init__(self, config_file):
        """
        init
        :param config_file: Application config file
        :return:
        """
        self.config = ConfigParser()
        self.config.read(config_file)
        self.session = Session(
            aws_access_key_id=self.config['aws']['access_key'],
            aws_secret_access_key=self.config['aws']['secret_access_key'],
            region_name=self.config['aws']['region']
        )
        self.s3 = self.session.resource('s3')
        self.s3client = self.session.client('s3')
        self.bucket_name = self.config['baseball_report']['bucket_name']

    def upload_files(self, dir_path, extension, key_name, delimiter='/', delete=True):
        """
        file upload for S3
        :param dir_path: input_file_path
        :param extension: upload file extension
        :param key_name: bucket key name
        :param delimiter: Delimiter
        :param delete: Delete Flg
        :return: None
        """
        for file_name in glob.glob(delimiter.join([dir_path, '*{extension}'.format(extension=extension)])):
            remote_file_name = delimiter.join(
                [
                    key_name,
                    file_name.replace('{dir_path}{delimiter}'.format(dir_path=dir_path, delimiter=delimiter), '')
                ]
            )
            self.s3client.upload_file(file_name, self.bucket_name, remote_file_name)
            if delete:
                os.remove(file_name)
