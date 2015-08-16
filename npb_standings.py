#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import urllib.request
from bs4 import BeautifulSoup
from configparser import ConfigParser


class NpbStandings(object):

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

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
            html = urllib.request.urlopen(self.config[league]['url'])
            soup = BeautifulSoup(html)
            table = soup.find('table', class_='NpbPlSt yjM')
            for tr in table.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text)
                dic_standings[league].append(row)
        return dic_standings

    def get_pythagorian(self, standings):
        for k, v in standings.items():
            print(k)
            for team in v:
                if len(team) < 15: continue
                print(team)


if __name__ == '__main__':
    st = NpbStandings()
    standings = st.get()
    standings_plus_pythagorian = st.get_pythagorian(standings)
    #print(result)
