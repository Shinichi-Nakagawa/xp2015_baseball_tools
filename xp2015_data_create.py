#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_standings import NpbStandings
from npb_batter_stats import NpbBatterStats
from service.storage import Storage

class Xp2015DataCreate(object):

    def __init__(self, config_file='app.ini'):
        self.storage_service = Storage(config_file)
        self.standing_service = NpbStandings()
        self.standings = self.standing_service.get()
        self.batting_stats_service = NpbBatterStats()
        self.batting_stats = self.batting_stats_service.get()

    def team_standings(self):
        """
        順位表取得
        :return:
        """
        self.standing_service.excel(
            self.standings,
            'xp_npb_ranking.{extension}'.format(extension=self.standing_service.extension),
            columns=['rank', 'team', 'win', 'lose', 'rs', 'ra', 'run_diff', 'win_p'],
            sort_key='rank',
            ascending=True,
        )

    def team_py_standings(self):
        """
        順位表取得(ピタゴラス勝率)
        :return:
        """
    # ピタゴラス勝率順
        self.standing_service.excel(
            self.standings,
            'xp_npb_py_ranking.{extension}'.format(extension=self.standing_service.extension),
            columns=['team', 'py_win', 'py_lose', 'rs', 'ra', 'run_diff', 'py_expectation', 'rank'],
            sort_key='py_expectation',
            ascending=False,
        )

    def ops(self):
        """
        OPSランキング
        :return:
        """
        self.batting_stats_service.excel(
            self.batting_stats,
            'xp_npb_batter_ops.{extension}'.format(extension=self.standing_service.extension),
            columns=['name_and_team', 'ops', 'obp', 'slg'],
            sort_key='ops',
            ascending=False
        )

    def dunn(self):
        """
        アダム・ダン率ランキング
        :return:
        """
        # アダム・ダン率ランキング
        self.batting_stats_service.excel(
            self.batting_stats,
            'xp_npb_batter_dunn.{extension}'.format(extension=self.standing_service.extension),
            columns=['name_and_team', 'dunn', 'hr', 'bb', 'so'],
            sort_key='dunn',
            ascending=False
        )

    def upload_files(self):
        """
        ファイル転送
        :return:
        """
        self.storage_service.upload_files(
            self.standing_service.output_path,
            self.standing_service.extension,
            self.standing_service.now_time
        )

def main():
    cl = Xp2015DataCreate()
    cl.team_standings()
    cl.team_py_standings()
    cl.ops()
    cl.dunn()
    cl.upload_files()

if __name__ == '__main__':
    main()
