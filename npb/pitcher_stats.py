#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb.data_source import DataSource
from baseball.stats import Stats

class PitcherStats(DataSource):

    def _calc_ip(self, ip, delimiter='\xa0'):
        """
        イニング計算
        :param ip: (str)inning pitched
        :param delimiter: default=no break space
        :return: (float)ip
        """
        ips = ip.split(delimiter)
        if len(ips) == 1:
            return float(ips[0])
        else:
            # 1/3 = 0.333, 2/3 = 0.666
            if ips[1] == '1/3':
                return float(ips[0]) + 0.333
            elif ips[1] == '2/3':
                return float(ips[0]) + 0.666
            else:
                raise Exception('イレギュラーなイニング数:{ip}'.format(ip=ip))

    def get_baseballdata_row(self, row, config_path):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :param config_path: config上の定義名
        :return: dict
        """
        config_pitcher = self.config[config_path]
        _stats = row

        # 名前と順位を分割
        rank, name = row['name'].split(':')
        _stats['name'] = name
        # イニングを計算し直す(分数表記から小数表記に)
        key_ip, type_ip = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=35)]
        )
        _stats[key_ip] = self._calc_ip(row['ip'],delimiter=' ')

        # 選手名(チーム名)
        key_name, type_name = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=36)]
        )
        _stats[key_name] = DataSource.get_player_name_and_team(name, row['team'])

        # 被アダム・ダン率
        key_dunn, type_dunn = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=37)]
        )
        _stats[key_dunn] = Stats.adam_dunn_pitcher(row['hr'], row['bb'], row['hbp'], row['so'], row['bf'])

        # 順位
        key_rank, type_rank = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=38)]
        )
        _stats[key_rank] = int(rank)

        return _stats

    def get_row(self, row, config_path):
        """
        行データ出力
        :param row: スクレイピングした結果の行データ
        :param config_path: config上の定義名
        :return: dict
        """
        config_pitcher = self.config[config_path]
        _stats = row
        # イニングを計算し直す(分数表記から小数表記に)
        key_ip, type_ip = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=29)]
        )
        _stats[key_ip] = self._calc_ip(row['ip'])

        # 選手名(チーム名)
        key_name, type_name = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=24)]
        )
        _stats[key_name] = DataSource.get_player_name_and_team(row['name'], row['team'])

        # BB/9
        key_bb9, type_bb9 = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=25)]
        )
        _stats[key_bb9] = Stats.bb9(row['bb'], _stats['calc_ip'])

        # SO/9
        key_so9, type_so9 = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=26)]
        )
        _stats[key_so9] = Stats.so9(row['so'], _stats['calc_ip'])

        # HR/9
        key_hr9, type_hr9 = DataSource.get_column_and_data_type(
            config_pitcher[PitcherStats.KEY_FORMAT.format(index=27)]
        )
        _stats[key_hr9] = Stats.so9(row['hr'], _stats['calc_ip'])

        return _stats

    def get(self, ):
        """
        投手成績を取得して吐き出す
        return : dict
        """
        return self.get_yahoo_japan_baseball('stats_pitcher_url', 'NpbPlSt mb10', 'pitcher', 23)

    def get_baseballdata(self, ):
        """
        投手成績を取得して吐き出す(baseballdata)
        return : dict
        :return:
        """
        return super(PitcherStats, self).get_baseballdata('stats_pitcher_baseballdata_url', 'responsive', 'pitcher_baseballdata', 35)


if __name__ == '__main__':
    st = PitcherStats(config_file='../config.ini')
    stats = st.get()
    stats2 = st.get_baseballdata()
    st.excel(stats, filename=r'npb_pitcher_stats.xlsx', output_dir='../output')
    st.excel(stats2, filename=r'npb_pitcher_stats_baseballdata.xlsx', output_dir='../output')
