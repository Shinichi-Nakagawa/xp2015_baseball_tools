#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser
from collections import OrderedDict


class NpbStats(object):
    # 出力結果のKey(confing.ini)
    KEY_FORMAT = 'key_{index}'

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    def _batter_stats(self, stats):
        """
        Team Stats
        :param row: Team Stats
        :return: list(team_stats + SABR)
        """
        _stats = stats
        # OPS
        key_ops = NpbStats.KEY_FORMAT.format(index=25)
        ops = round(float(stats['obp']) + float(stats['slg']), 3)
        _stats[self.config['batter'][key_ops]] = ops
        # Adam dunn
        key_dunn = NpbStats.KEY_FORMAT.format(index=26)
        dunn = round((float(stats['hr']) + float(stats['bb']) + float(stats['so'])) / float(stats['atbat']) * 100, 1)
        _stats[self.config['batter'][key_dunn]] = dunn
        return _stats

    def get(self, ):
        """
        順位表を取得して吐き出す
        return : dict
        """
        dic_stats = {
            'central': [],
            'pacific': [],
        }
        for league in dic_stats.keys():
            html = urllib.request.urlopen(self.config[league]['stats_batter_url'])
            soup = BeautifulSoup(html)
            table = soup.find('table', class_='NpbPlSt mb10')
            for tr in table.find_all('tr'):
                row = OrderedDict()
                for i, td in enumerate(tr.find_all('td')):
                    key = NpbStats.KEY_FORMAT.format(index=i)
                    row[self.config['batter'][key]] = td.text
                if len(row) < 24:
                    continue
                dic_stats[league].append(self._batter_stats(row))
        return dic_stats

    def excel(self, standings, filename=r'npb_batter_stats_{league}.xlsx'):
        for k, v in standings.items():
            df = pd.DataFrame(v)
            df.to_excel(filename.format(league=k), 'batter_stats')


if __name__ == '__main__':
    from pprint import pprint
    st = NpbStats()
    standings = st.get()
    #pprint(standings)
    st.excel(standings)
