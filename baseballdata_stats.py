#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb.pitcher_stats import PitcherStats

class BaseballdataStats(object):

    def __init__(self):
        self.pitching_stats_service = PitcherStats()
        self.pitching_stats_data = self.pitching_stats_service.get_baseballdata()

    def dunn(self):
        """
        アダム・ダン率ランキング
        :return:
        """
        # アダム・ダン率ランキング
        self.pitching_stats_service.excel(
            self.pitching_stats_data,
            'xp_npb_pitcher_dunn.{extension}'.format(extension=self.pitching_stats_service.extension),
            columns=['name_and_team', 'dunn', 'hr', 'bb', 'so', 'hbp', 'bf', 'era', 'win', 'lose'],
            sort_key='dunn',
            ascending=False
        )

def main():
    cl = BaseballdataStats()
    cl.dunn()

if __name__ == '__main__':
    main()
