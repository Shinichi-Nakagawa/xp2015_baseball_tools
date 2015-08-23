#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_data import NpbData

class NpbStandings(NpbData):

    # ピタゴラス勝率のべき乗
    PYTHAGORIAN_POWER = 2.0

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

    def get_row(self, row):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :return: dict
        """
        team_stats = row
        # 順位を書き換え('位'を抜く)
        key_rank = NpbStandings.KEY_FORMAT.format(index=0)
        rank = int(row[self.config['standings'][key_rank]].replace('位', ''))
        team_stats[self.config['standings'][key_rank]] = rank
        # ピタゴラス勝率を追加
        key_py_ex = NpbStandings.KEY_FORMAT.format(index=15)
        py_ex = NpbStandings.calc_pythagorean_expectation(float(row['rs']), float(row['ra']))
        team_stats[self.config['standings'][key_py_ex]] = py_ex
        # ピタゴラス勝利数
        key_py_win = NpbStandings.KEY_FORMAT.format(index=16)
        py_win = int(round(float(row['game']) * py_ex, 0))
        team_stats[self.config['standings'][key_py_win]] = py_win
        # ピタゴラス敗戦数
        key_py_lose = NpbStandings.KEY_FORMAT.format(index=17)
        py_lose = int(row['game']) - py_win
        team_stats[self.config['standings'][key_py_lose]] = py_lose
        # 得失点差
        key_run_diff = NpbStandings.KEY_FORMAT.format(index=18)
        run_diff = int(row['rs']) - int(row['ra'])
        team_stats[self.config['standings'][key_run_diff]] = run_diff
        return team_stats

    def get(self, ):
        """
        順位表を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('standings_url', 'NpbPlSt yjM', 'standings', 15)


if __name__ == '__main__':
    st = NpbStandings()
    standings = st.get()
    st.excel(standings, filename=r'npb_standings_{league}.xlsx')
