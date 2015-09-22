#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb.team_standings import TeamStandings
from npb.batter_stats import BatterStats
from npb.pitcher_stats import PitcherStats

if __name__ == '__main__':
    config_file = './config/config.ini'
    st = TeamStandings(config_file=config_file)
    standings = st.get()
    # ピタゴラス勝率順
    # ピタゴラス勝率,ピタゴラス勝利,ピタゴラス敗北(試合数-ピタゴラス勝利),得点,失点,得失点差
    st.excel(
        standings,
        'npb_py_ranking.xlsx',
        columns=['team', 'py_expectation', 'py_win', 'py_lose', 'rs', 'ra', 'run_diff'],
        sort_key='py_expectation',
        ascending=False,
    )

    # 打撃成績+セイバーメトリクス
    # 打率,本塁打,打点,出塁率,長打率,OPS,ISO
    batter = BatterStats(config_file=config_file)
    stats_batter = batter.get()
    batter.excel(
        stats_batter,
        'npb_batter_stats_sabr.xlsx',
        columns=['name_and_team', 'ba', 'hr', 'rbi', 'obp', 'slg', 'ops', 'iso'],
        sort_key='ba',
        ascending=False,
    )

    # 投手成績+セイバーメトリクス
    # 防御率,奪三振,勝,負,奪三振率,与四球率,被本塁打率
    pitcher = PitcherStats(config_file=config_file)
    stats_pitcher = pitcher.get()
    pitcher.excel(
        stats_pitcher,
        'npb_pitcher_stats_sabr.xlsx',
        columns=['name_and_team', 'era', 'so', 'win', 'lose', 'k9', 'bb9', 'hr9'],
        sort_key='era',
        ascending=True,
    )
