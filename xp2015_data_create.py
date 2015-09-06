#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_standings import NpbStandings
from npb_batter_stats import NpbBatterStats
from service.storage import Storage

if __name__ == '__main__':
    storage_service = Storage('app.ini')
    st = NpbStandings()
    standings = st.get()
    # 順位表
    st.excel(
        standings,
        'xp_npb_ranking.{extension}'.format(extension=st.extension),
        columns=['rank', 'team', 'win', 'lose', 'rs', 'ra', 'run_diff', 'win_p'],
        sort_key='rank',
        ascending=True,
    )
    # ピタゴラス勝率順
    st.excel(
        standings,
        'xp_npb_py_ranking.{extension}'.format(extension=st.extension),
        columns=['team', 'py_win', 'py_lose', 'rs', 'ra', 'run_diff', 'py_expectation', 'rank'],
        sort_key='py_expectation',
        ascending=False,
    )

    bt = NpbBatterStats()
    batters = bt.get()
    # OPSランキング
    bt.excel(
        batters,
        'xp_npb_batter_ops.{extension}'.format(extension=st.extension),
        columns=['name_and_team', 'ops', 'obp', 'slg'],
        sort_key='ops',
        ascending=False
    )
    # アダム・ダン率ランキング
    bt.excel(
        batters,
        'xp_npb_batter_dunn.{extension}'.format(extension=st.extension),
        columns=['name_and_team', 'dunn', 'hr', 'bb', 'so'],
        sort_key='dunn',
        ascending=False
    )

    # S3に転送
    storage_service.upload_files(st.output_path, st.extension, st.now_time)
