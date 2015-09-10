#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from datetime import datetime, timedelta
import math


class JobSettings(object):
    """
    出力設定
    """

    def __init__(self, crontab):
        """
        :param crontab: crontab.CronTab
        """
        self._crontab = crontab

    def schedule(self):
        """
        次回実行
        :return: datetime
        """
        crontab = self._crontab
        return datetime.now() + timedelta(seconds=math.ceil(crontab.next()))

    def interval(self):
        """
        次回実行までの時間
        :return: seconds
        """
        crontab = self._crontab
        return math.ceil(crontab.next())