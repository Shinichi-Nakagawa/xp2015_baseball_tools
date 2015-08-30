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
        config_standings = self.config['standings']
        team_stats = row
        # 順位を書き換え('位'を抜く)
        key_rank, type_rank = NpbData.get_column_and_data_type(
            config_standings[NpbStandings.KEY_FORMAT.format(index=0)]
        )
        team_stats[key_rank] = NpbData.get_value(type_rank, row[key_rank].replace('位', ''))

        # ピタゴラス勝率を追加
        key_py_ex, type_py_ex = NpbData.get_column_and_data_type(
            config_standings[NpbStandings.KEY_FORMAT.format(index=15)]
        )
        team_stats[key_py_ex] = NpbStandings.calc_pythagorean_expectation(float(row['rs']), float(row['ra']))

        # ピタゴラス勝利数
        key_py_win, type_py_win = NpbData.get_column_and_data_type(
            config_standings[NpbStandings.KEY_FORMAT.format(index=16)]
        )
        team_stats[key_py_win] = NpbData.get_value(type_py_win, round(float(row['game']) * team_stats[key_py_ex], 0))

        # ピタゴラス敗戦数
        key_py_lose, type_py_lose = NpbData.get_column_and_data_type(
            config_standings[NpbStandings.KEY_FORMAT.format(index=17)]
        )
        team_stats[key_py_lose] = row['game'] - team_stats[key_py_win]

        # 得失点差
        key_run_diff, type_run_diff = NpbData.get_column_and_data_type(
            config_standings[NpbStandings.KEY_FORMAT.format(index=18)]
        )
        team_stats[key_run_diff] = row['rs'] - row['ra']
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
    st.excel(standings, filename=r'npb_standings.xlsx')
