#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_data import NpbData
from baseball.stats import Stats

class NpbPitcherStats(NpbData):

    def get_row(self, row):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :return: dict
        """
        config_pitcher = self.config['pitcher']
        _stats = row
        # イニングを計算し直す(分数表記から小数表記に)
        key_ip, type_ip = NpbData.get_column_and_data_type(
            config_pitcher[NpbPitcherStats.KEY_FORMAT.format(index=29)]
        )
        ips = row['ip'].split('\xa0')
        if len(ips) == 1:
            _stats[key_ip] = float(ips[0])
        else:
            # 1/3 = 0.333, 2/3 = 0.666
            if ips[1] == '1/3':
                _stats[key_ip] = float(ips[0]) + 0.333
            elif ips[1] == '2/3':
                _stats[key_ip] = float(ips[0]) + 0.666
            else:
                raise Exception('イレギュラーなイニング数:{ip}'.format(ip=row['ip']))

        # 選手名(チーム名)
        key_name, type_name = NpbData.get_column_and_data_type(
            config_pitcher[NpbPitcherStats.KEY_FORMAT.format(index=24)]
        )
        _stats[key_name] = '{name}({team})'.format(name=row['name'].replace('　', ''), team=row['team'])

        # BB/9
        key_bb9, type_bb9 = NpbData.get_column_and_data_type(
            config_pitcher[NpbPitcherStats.KEY_FORMAT.format(index=25)]
        )
        _stats[key_bb9] = Stats.bb9(row['bb'], _stats['calc_ip'])

        # SO/9
        key_so9, type_so9 = NpbData.get_column_and_data_type(
            config_pitcher[NpbPitcherStats.KEY_FORMAT.format(index=26)]
        )
        _stats[key_so9] = Stats.so9(row['so'], _stats['calc_ip'])

        # HR/9
        key_hr9, type_hr9 = NpbData.get_column_and_data_type(
            config_pitcher[NpbPitcherStats.KEY_FORMAT.format(index=27)]
        )
        _stats[key_hr9] = Stats.so9(row['hr'], _stats['calc_ip'])

        return _stats

    def get(self, ):
        """
        投手成績を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('stats_pitcher_url', 'NpbPlSt mb10', 'pitcher', 23)


if __name__ == '__main__':
    st = NpbPitcherStats()
    stats = st.get()
    st.excel(stats, filename=r'npb_pitcher_stats_{league}.xlsx')
