#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from npb.team_standings import TeamStandings
from npb.batter_stats import BatterStats
from npb.pitcher_stats import PitcherStats
from npb.models.yahoo import Yahoo, YahooTeamStandings, YahooBatterStats, YahooPitcherStats
from service.database import Database
import json

class NpbDataCreate(object):

    def __init__(self, config_file="./config/database.ini"):
        self.database = Database(config_file=config_file)
        self.yahoo = Yahoo()
        self.yahoo.table(self.database.metadata)
        self.database.mapping(self.yahoo.table_class_list())
        self.database.create_table()

    def create_team_standings(self):
        service = TeamStandings()
        values = []
        for league, stats in service.get().items():
            for team_stats in stats:
                values.append(
                    YahooTeamStandings(
                        service.now_time,
                        league,
                        team_stats['team'],
                        json.dumps(team_stats, ensure_ascii=False),
                    )
                )
        self.add_all(values)

    def create_player_standings(self, service_class, player_class):
        service = service_class()
        values = []
        for league, stats in service.get().items():
            for team_stats in stats:
                values.append(
                    player_class(
                        service.now_time,
                        league,
                        team_stats['team'],
                        team_stats['name'],
                        json.dumps(team_stats, ensure_ascii=False))
                )
        self.add_all(values)

    def add_all(self, values):
        try:
            self.database.session.add_all(values)
        except:
            self.database.session.rollback()
        finally:
            self.database.session.commit()




def main():
    cl = NpbDataCreate()
    cl.create_team_standings()
    #cl.create_player_standings(BatterStats, YahooBatterStats)
    #cl.create_player_standings(PitcherStats, YahooPitcherStats)

if __name__ == '__main__':
    main()
