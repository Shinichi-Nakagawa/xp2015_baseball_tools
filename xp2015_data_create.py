#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_standings import NpbStandings
from npb_batter_stats import NpbBatterStats

if __name__ == '__main__':
    st = NpbStandings()
    standings = st.get()
    # 順位表
    st.excel(
        standings,
        'npb_ranking_{league}.xlsx',
        columns=['rank', 'team', 'win', 'lose', 'rs', 'ra', 'run_diff', 'win_p'],
        sort_key='rank',
        ascending=True,
    )
    # ピタゴラス勝率順
    st.excel(
        standings,
        'npb_py_ranking_{league}.xlsx',
        columns=['team', 'py_win', 'py_lose', 'rs', 'ra', 'run_diff', 'py_expectation', 'rank'],
        sort_key='py_expectation',
        ascending=False,
    )

    bt = NpbBatterStats()
    batters = bt.get()
    # OPSランキング
    bt.excel(
        batters,
        'npb_batter_ops_{league}.xlsx',
        columns=['name_and_team', 'ops', 'obp', 'slg'],
        sort_key='ops',
        ascending=False
    )
    # アダム・ダン率ランキング
    bt.excel(
        batters,
        'npb_batter_dunn_{league}.xlsx',
        columns=['name_and_team', 'dunn', 'hr', 'bb', 'so'],
        sort_key='dunn',
        ascending=False
    )
