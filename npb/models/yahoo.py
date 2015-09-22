#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'


from sqlalchemy import Table, Column, String, Text, Date, DateTime


class Yahoo(object):
    """
    Baseball Stats by Yahoo Japan Sports
    """

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, now_date):
        self.team_standings = None
        self.batter_stats = None
        self.pitcher_stats = None
        self.now_date = now_date

    @classmethod
    def _mapping(cls, mapper_class, table):
        """
        O/R mapping
        :param mapper_class: Mapper Class
        :param table: Table Object
        :return: {"mapper_class": Mapper Class, "table": Table Object}
        """
        return {"mapper_class": mapper_class, "table": table}

    def table_class_list(self):
        """
        table - class mapping list
        :return:
        """
        return (
            Yahoo._mapping(YahooTeamStandings, self.team_standings),
            Yahoo._mapping(YahooBatterStats, self.batter_stats),
            Yahoo._mapping(YahooPitcherStats, self.pitcher_stats)
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
            Column("date_time", Date, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("stats", Text, nullable=False),
            Column("create_at", DateTime, default=self.now_date),
            Column("update_at", DateTime, default=self.now_date),
        )
        self.batter_stats = Table(
            "yahoo_batter_stats",
            metadata,
            Column("date_time", Date, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("player_name", String(128), primary_key=True),
            Column("stats", Text, nullable=False),
            Column("create_at", DateTime, default=self.now_date),
            Column("update_at", DateTime, default=self.now_date),
        )
        self.pitcher_stats = Table(
            "yahoo_pitcher_stats",
            metadata,
            Column("date_time", Date, primary_key=True),
            Column("league", String(8), primary_key=True),
            Column("team", String(64), primary_key=True),
            Column("player_name", String(128), primary_key=True),
            Column("stats", Text, nullable=False),
            Column("create_at", DateTime, default=self.now_date),
            Column("update_at", DateTime, default=self.now_date),
        )

class YahooTeamStandings(object):
    """
    Team Stats by Yahoo Japan Sports
    """

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
    """
    Player Stats by Yahoo Japan Sports
    """

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
    """
    Batter Stats by Yahoo Japan Sports
    """

    def __repr__(self):
        return "<YahooBatterStats({date_time}, {league}, {team}, {player_name}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            player_name=self.player_name,
            stats=self.stats
        )


class YahooPitcherStats(YahooPlayerStats):
    """
    Pitcher Stats by Yahoo Japan Sports
    """

    def __repr__(self):
        return "<YahooPitcherStats({date_time}, {player_name}, {stats})>".format(
            date_time=self.date_time.strftime(Yahoo.DATE_FORMAT),
            league=self.league,
            team=self.team,
            player_name=self.player_name,
            stats=self.stats
        )
