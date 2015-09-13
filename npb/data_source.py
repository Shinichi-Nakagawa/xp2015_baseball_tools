#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser
from collections import OrderedDict
from datetime import datetime as dt
import time
from datetime import timezone, timedelta

class DataSource(object):
    # 出力結果のKey(confing.ini)
    KEY_FORMAT = 'key_{index}'
    DATETIME_FORMAT = '%Y%m%d_%H%M%S'

    def __init__(self, config_file='config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)
        self.output_path = self.config['config']['output_path']
        self.extension = self.config['config']['extension']
        loc = dt.fromtimestamp(time.time(), self._get_timezone())
        self.now_time = loc.strftime(DataSource.DATETIME_FORMAT)

    def _get_timezone(self):
        """
        タイムゾーン取得
        :return: now time
        """
        return timezone(
            timedelta(hours=+int(self.config['config']['hours'])),
            self.config['config']['timezone']
        )

    def get_row(self, row, config_path):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :param config_path: config上の定義名
        :return: dict
        """
        # サブクラスで実装
        pass

    def get_baseballdata_row(self, row, config_path):
        """
        行データ出力(データで楽しむプロ野球)
        :param row: スクレイピングした結果の行データ
        :param config_path: config上の定義名
        :return: dict
        """
        # サブクラスで実装
        pass

    @classmethod
    def get_column_and_data_type(cls, config_value):
        """
        カラム名とデータ型を取得
        :param config_value: config.iniのパラメータ
        :return: column, data_type
        """
        return config_value.split(',')

    @classmethod
    def get_value(cls, data_type, text):
        """
        データ型に合わせて置換
        :param data_type: data type
        :param text: value text
        :return: (data type)text
        """
        if data_type is 'i':
            return int(text)
        elif data_type is 'f':
            return float(text)

        return text

    def get_baseballdata(self, config_url, table_class, config_path, column_size):
        """
        データで楽しむプロ野球をスクレイピング
        :param config_url: config上のurl定義名
        :param table_class: スクレイピングするテーブルのクラス名
        :param config_path: config上の定義名
        :param column_size: カラム数
        :return:
        """
        scraping_dict = {
            'central': [],
            'pacific': [],
        }
        for league in scraping_dict.keys():
            html = urllib.request.urlopen(self.config[league][config_url])
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', class_=table_class)
            for tr in table.find_all('tr'):
                row = OrderedDict()
                if len(tr.find_all('td')) < column_size:
                    continue
                for i, td in enumerate(tr.find_all('td')):
                    key = DataSource.KEY_FORMAT.format(index=i)
                    column, data_type = DataSource.get_column_and_data_type(self.config[config_path][key])
                    row[column] = DataSource.get_value(data_type, td.text.strip())
                    if len(row) == column_size:
                        break
                scraping_dict[league].append(self.get_baseballdata_row(row, config_path))
        return scraping_dict

    def get_yahoo_japan_baseball(self, config_url, table_class, config_path, column_size):
        """
        Yahoo Japan Baseballをスクレイピング
        :param config_url: config上のurl定義名
        :param table_class: スクレイピングするテーブルのクラス名
        :param config_path: config上の定義名
        :param column_size: カラム数
        :return:
        """
        scraping_dict = {
            'central': [],
            'pacific': [],
        }
        for league in scraping_dict.keys():
            html = urllib.request.urlopen(self.config[league][config_url])
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', class_=table_class)
            for tr in table.find_all('tr'):
                row = OrderedDict()
                if len(tr.find_all('td')) < column_size:
                    continue
                for i, td in enumerate(tr.find_all('td')):
                    key = DataSource.KEY_FORMAT.format(index=i)
                    column, data_type = DataSource.get_column_and_data_type(self.config[config_path][key])
                    row[column] = DataSource.get_value(data_type, td.text.strip())
                scraping_dict[league].append(self.get_row(row, config_path))
        return scraping_dict

    def excel(self, scraping_dict, filename, columns=None, sort_key='rank', ascending=True, output_dir=None):
        """
        Excel出力(league毎にシートを出力)
        :param scraping_dict: スクレイピング結果
        :param filename: book名
        :param columns: カラム名
        :param sort_key: ソート用のキー
        :param ascending: ソート順(デフォルトは昇順)
        :param output_dir: 出力先ディレクトリ
        :return: None
        """
        if output_dir is None:
            output_dir = self.output_path

        writer = pd.ExcelWriter('/'.join([output_dir, filename]))
        for k, v in scraping_dict.items():
            df = pd.DataFrame(v)
            if columns is None:
                df.to_excel(writer, k)
            else:
                df[columns].sort(sort_key, ascending=ascending).to_excel(writer, k)

        writer.save()
