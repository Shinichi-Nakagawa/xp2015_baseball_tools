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
        _stats = row
        # OPS
        key_ops = NpbStats.KEY_FORMAT.format(index=25)
        ops = round(float(row['obp']) + float(row['slg']), 3)
        _stats[self.config['batter'][key_ops]] = ops
        # Adam dunn
        key_dunn = NpbStats.KEY_FORMAT.format(index=26)
        dunn = round((float(row['hr']) + float(row['bb']) + float(row['so'])) / float(row['pa']) * 100, 1)
        _stats[self.config['batter'][key_dunn]] = dunn
        # 選手名(チーム名)
        key_name = NpbStats.KEY_FORMAT.format(index=27)
        name = '{name}({team})'.format(name=row['name'].replace('　', ''), team=row['team'])
        _stats[self.config['batter'][key_name]] = name
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
