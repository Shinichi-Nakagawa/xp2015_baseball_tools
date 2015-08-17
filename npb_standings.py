#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser
from collections import OrderedDict


class NpbStandings(object):

    # ピタゴラス勝率のべき乗
    PYTHAGORIAN_POWER = 2.0
    # 出力結果のKey(confing.ini)
    KEY_FORMAT = 'key_{index}'

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    @classmethod
    def calc_pythagorean_expectation(cls, r, ra):
        """
        ピタゴラス勝率
        :param r: Runs Scored
        :param ra: Runs Allowed
        :return: pythagorean expectation
        """
        r_power = r ** NpbStandings.PYTHAGORIAN_POWER
        ra_power = ra ** NpbStandings.PYTHAGORIAN_POWER
        return round(r_power / (r_power + ra_power), 3)

    def _team_stats(self, stats):
        """
        Team Stats
        :param row: Team Stats
        :return: list(team_stats + SABR)
        """
        team_stats = stats
        # ピタゴラス勝率を追加
        key_py_ex = NpbStandings.KEY_FORMAT.format(index=15)
        py_ex = NpbStandings.calc_pythagorean_expectation(float(stats['rs']), float(stats['ra']))
        team_stats[self.config['standings'][key_py_ex]] = py_ex
        # ピタゴラス勝利数
        key_py_win = NpbStandings.KEY_FORMAT.format(index=16)
        py_win = int(round(float(stats['game']) * py_ex, 0))
        team_stats[self.config['standings'][key_py_win]] = py_win
        # ピタゴラス敗戦数
        key_py_lose = NpbStandings.KEY_FORMAT.format(index=17)
        py_lose = int(stats['game']) - py_win
        team_stats[self.config['standings'][key_py_lose]] = py_lose
        return team_stats

    def get(self, ):
        """
        順位表を取得して吐き出す
        return : dict
        """
        dic_standings = {
            'central': [],
            'pacific': [],
        }
        for league in dic_standings.keys():
            html = urllib.request.urlopen(self.config[league]['standings_url'])
            soup = BeautifulSoup(html)
            table = soup.find('table', class_='NpbPlSt yjM')
            for tr in table.find_all('tr'):
                row = OrderedDict()
                for i, td in enumerate(tr.find_all('td')):
                    key = NpbStandings.KEY_FORMAT.format(index=i)
                    row[self.config['standings'][key]] = td.text
                if len(row) < 15:
                    continue
                dic_standings[league].append(self._team_stats(row))
        return dic_standings

    def excel(self, standings, filename=r'npb_standings_{league}.xlsx'):
        for k, v in standings.items():
            df = pd.DataFrame(v)
            df.to_excel(filename.format(league=k), 'standings')


if __name__ == '__main__':
    from pprint import pprint
    st = NpbStandings()
    standings = st.get()
    #pprint(standings)
    st.excel(standings)
