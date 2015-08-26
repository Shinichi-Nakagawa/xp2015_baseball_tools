#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_data import NpbData

class NpbStats(NpbData):

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
            config_batter[NpbStats.KEY_FORMAT.format(index=25)]
        )
        _stats[key_ops] = round(row['obp'] + row['slg'], 3)

        # Adam dunn
        key_dunn, type_dunn = NpbData.get_column_and_data_type(
            config_batter[NpbStats.KEY_FORMAT.format(index=26)]
        )
        _stats[key_dunn] = round((float(row['hr']) + float(row['bb']) + float(row['so'])) / float(row['pa']) * 100, 1)

        # 選手名(チーム名)
        key_name, type_name = NpbData.get_column_and_data_type(
            config_batter[NpbStats.KEY_FORMAT.format(index=27)]
        )
        _stats[key_name] = '{name}({team})'.format(name=row['name'].replace('　', ''), team=row['team'])
        return _stats

    def get(self, ):
        """
        順位表を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('stats_batter_url', 'NpbPlSt mb10', 'batter', 24)


if __name__ == '__main__':
    st = NpbStats()
    stats = st.get()
    st.excel(stats, filename=r'npb_batter_stats_{league}.xlsx')
