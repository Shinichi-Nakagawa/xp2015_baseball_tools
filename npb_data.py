#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser
from collections import OrderedDict


class NpbData(object):
    # 出力結果のKey(confing.ini)
    KEY_FORMAT = 'key_{index}'

    def __init__(self, config_file='config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_row(self, row):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :return: dict
        """
        # サブクラスで実装
        pass

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
                for i, td in enumerate(tr.find_all('td')):
                    key = NpbData.KEY_FORMAT.format(index=i)
                    row[self.config[config_path][key]] = td.text
                if len(row) < column_size:
                    continue
                scraping_dict[league].append(self.get_row(row))
        return scraping_dict

    def excel(self, scraping_dict, filename, sheet_name='stats', columns=None, sort_key='rank', ascending=True):
        """
        Excel出力
        :param scraping_dict: スクレイピング結果
        :param filename: book名
        :param sheet_name: sheet名
        :param columns: カラム名
        :param sort_key: ソート用のキー
        :param ascending: ソート順(デフォルトは昇順)
        :return: None
        """
        for k, v in scraping_dict.items():
            df = pd.DataFrame(v)
            if columns is None:
                df.to_excel(filename.format(league=k), sheet_name)
            else:
                df[columns].sort(sort_key, ascending=ascending).to_excel(filename.format(league=k), sheet_name)
