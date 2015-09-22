#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'


from sqlalchemy import Table, Column, String, Text, DateTime


class Yahoo(object):

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        pass

    def _mapping(self, mapper_class, table):
        return {"mapper_class": mapper_class, "table": table}

    def table_class_list(self):
        return (
            self._mapping(YahooTeamStandings, self.team_standings),
            self._mapping(YahooBatterStats, self.batter_stats),
            self._mapping(YahooPitcherStats, self.pitcher_stats)
        )

    def table(self, metadata):
        """
        table
        :param metadata: sqlalchemy metadata
        :return:
        """
        self.team_standings = Table(
            "yahoo_team_standings",
            metadata,
            Column("date_time", DateTime, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("stats", Text, nullable=False)
        )
        self.batter_stats = Table(
            "yahoo_batter_stats",
            metadata,
            Column("date_time", DateTime, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("player_name", String(128), primary_key=True),
            Column("stats", Text, nullable=False)
        )
        self.pitcher_stats = Table(
            "yahoo_pitcher_stats",
            metadata,
            Column("date_time", DateTime, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("player_name", String(128), primary_key=True),
            Column("stats", Text, nullable=False)
        )

class YahooTeamStandings(object):

    def __init__(self, date_time, league, team, stats):
        """
        initialize
        :param date_time: now time
        :param league: league name
        :param team: team name
        :param stats: team stats
        :return: None
        """
        self.date_time = date_time
        self.league = league
        self.team = team
        self.stats = stats

    def __repr__(self):
        return "<YahooTeamStandings({date_time}, {league}, {team}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            stats=self.stats
        )


class YahooPlayerStats(object):

    def __init__(self, date_time, league, team, player_name, stats):
        """
        initialize
        :param date_time: now time
        :param league: league name
        :param team: team name
        :param player_name: player name
        :param stats: team stats
        :return: None
        """
        self.date_time = date_time
        self.league = league
        self.team = team
        self.player_name = player_name
        self.stats = stats

    def __repr__(self):
        return "<YahooPlayerStats({date_time}, {league}, {team}, {player_name}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            player_name=self.player_name,
            stats=self.stats
        )


class YahooBatterStats(YahooPlayerStats):

    def __repr__(self):
        return "<YahooBatterStats({date_time}, {league}, {team}, {player_name}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            player_name=self.player_name,
            stats=self.stats
        )


class YahooPitcherStats(YahooPlayerStats):

    def __repr__(self):
        return "<YahooPitcherStats({date_time}, {player_name}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            player_name=self.player_name,
            stats=self.stats
        )
