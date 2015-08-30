#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_data import NpbData
from baseball.stats import Stats

class NpbBatterStats(NpbData):

    def get_row(self, row):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :return: dict
        """
        config_batter = self.config['batter']
        _stats = row
        # OPS
        key_ops, type_ops = NpbData.get_column_and_data_type(
            config_batter[NpbBatterStats.KEY_FORMAT.format(index=25)]
        )
        _stats[key_ops] = round(row['obp'] + row['slg'], 3)

        # Adam dunn
        key_dunn, type_dunn = NpbData.get_column_and_data_type(
            config_batter[NpbBatterStats.KEY_FORMAT.format(index=26)]
        )
        _stats[key_dunn] = Stats.adam_dunn_batter(row['hr'], row['bb'], row['so'], row['pa'])

        # 選手名(チーム名)
        key_name, type_name = NpbData.get_column_and_data_type(
            config_batter[NpbBatterStats.KEY_FORMAT.format(index=27)]
        )
        _stats[key_name] = '{name}({team})'.format(name=row['name'].replace('　', ''), team=row['team'])

        # iso
        key_iso, type_iso = NpbData.get_column_and_data_type(
            config_batter[NpbBatterStats.KEY_FORMAT.format(index=28)]
        )
        _stats[key_iso] = round(row['slg'] - row['ba'], 3)

        # BABIP
        key_babip, type_babip = NpbData.get_column_and_data_type(
            config_batter[NpbBatterStats.KEY_FORMAT.format(index=29)]
        )
        # シングルヒットの数を数えた後、BABIPを算出
        _single_hit = Stats.single(row['h'], row['hr'], row['_2b'], row['_3b'])
        _stats[key_babip] = Stats.babip(_single_hit, row['hr'], row['atbat'], row['so'], row['sf'])

        return _stats

    def get(self, ):
        """
        打者成績を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('stats_batter_url', 'NpbPlSt mb10', 'batter', 25)


if __name__ == '__main__':
    st = NpbBatterStats()
    stats = st.get()
    st.excel(stats, filename=r'npb_batter_stats_{league}.xlsx')
