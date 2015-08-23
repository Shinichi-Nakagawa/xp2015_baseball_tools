#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb_standings import NpbStandings

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
