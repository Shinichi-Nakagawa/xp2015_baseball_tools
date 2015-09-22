#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'


from configparser import ConfigParser
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, mapper

class Database(object):

    def __init__(self, config_file='../config/database.ini', database_engine='mysql'):
        config = ConfigParser()
        config.read(config_file)
        params = dict(config[database_engine])
        connection = "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}?charset={encoding}"\
            .format(**params)
        self.encoding = params.get('encoding')
        self.engine = create_engine(connection, encoding=self.encoding)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
        self.conn = self.engine.connect()
        self.metadata = MetaData()

    def create_table(self):
        """
        Create Table
        :return: None
        """
        self.metadata.create_all(self.engine)

    def connect(self):
        """
        Dabatase Connect
        :return: connection object
        """
        return self.engine.connect()

    def disconnect(self, conn):
        """
        Database Close
        :param conn:
        :return:
        """
        conn.close()

    def mapping(self, table_class_list):
        """
        O/R mapping
        :param table_class_list: list({"table": hoge, "mapper_class": hogeClass})
        :return: None
        """
        for table_class in table_class_list:
            mapper(table_class['mapper_class'], table_class["table"])
