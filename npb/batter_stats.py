#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb.data_source import DataSource
from baseball.stats import Stats

class BatterStats(DataSource):

    def get_row(self, row, config_path):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :param config_path: config上の定義名
        :return: dict
        """
        config_batter = self.config[config_path]
        _stats = row
        # OPS
        key_ops, type_ops = DataSource.get_column_and_data_type(
            config_batter[BatterStats.KEY_FORMAT.format(index=25)]
        )
        _stats[key_ops] = round(row['obp'] + row['slg'], 3)

        # Adam dunn
        key_dunn, type_dunn = DataSource.get_column_and_data_type(
            config_batter[BatterStats.KEY_FORMAT.format(index=26)]
        )
        _stats[key_dunn] = Stats.adam_dunn_batter(row['hr'], row['bb'], row['so'], row['pa'])

        # 選手名(チーム名)
        key_name, type_name = DataSource.get_column_and_data_type(
            config_batter[BatterStats.KEY_FORMAT.format(index=27)]
        )
        _stats[key_name] = DataSource.get_player_name_and_team(row['name'], row['team'])

        # iso
        key_iso, type_iso = DataSource.get_column_and_data_type(
            config_batter[BatterStats.KEY_FORMAT.format(index=28)]
        )
        _stats[key_iso] = round(row['slg'] - row['ba'], 3)

        # BABIP
        key_babip, type_babip = DataSource.get_column_and_data_type(
            config_batter[BatterStats.KEY_FORMAT.format(index=29)]
        )
        _stats[key_babip] = Stats.babip(row['h'], row['hr'], row['atbat'], row['so'], row['sf'])

        return _stats

    def get(self, ):
        """
        打者成績を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('stats_batter_url', 'NpbPlSt mb10', 'batter', 25)


if __name__ == '__main__':
    st = BatterStats('../config/config.ini')
    stats = st.get()
    st.excel(stats, filename=r'npb_batter_stats.xlsx', output_dir='../output')
