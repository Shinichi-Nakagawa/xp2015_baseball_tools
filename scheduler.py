#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from crontab import CronTab
from datetime import datetime, timedelta
import logging
import math
from multiprocessing import Pool
import time
from xp2015_data_create import Xp2015DataCreate


class JobSettings(object):
    """
    出力設定
    """

    def __init__(self, crontab, job):
        """
        :param crontab: crontab.CronTab
        :param job: function
        """
        self._crontab = crontab
        self.job = job

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


class JobController(object):
    """
    ジョブ実行Controller
    """

    @classmethod
    def run(cls, job_settings):
        """
        処理実行
        :param job_settings: JobSetings
        """

        logging.info("->- Process Start")
        while True:
            try:
                logging.info(
                    "-?- next running\tschedule:%s" %
                    job_settings.schedule().strftime("%Y-%m-%d %H:%M:%S")
                )
                time.sleep(job_settings.interval())
                logging.info("->- Job Start")
                job_settings.job()
                logging.info("-<- Job Done")
            except KeyboardInterrupt:
                break
        logging.info("-<- Process Done.")


def xp2015_data_create():
    """
    XP祭り2015用データ作成
    :return:
    """
    logging.info("->- XP2015 Data Create Start")
    # 実行モジュール
    cl = Xp2015DataCreate()
    cl.team_standings()
    cl.team_py_standings()
    cl.ops()
    cl.dunn()
    logging.info("-<- XP2015 Data Create Done.")
    logging.info("->- XP2015 Data Upload Start")
    cl.upload_files()
    logging.info("-<- XP2015 Data Upload Done.")


def main():
    """
    running
    :return: None
    """
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format="time:%(asctime)s.%(msecs)03d\tprocess:%(process)d" + "\tmessage:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # crontab settings
    job_settings = [
        JobSettings(CronTab("00 22 * * *"), xp2015_data_create),
    ]

    # multi process running
    p = Pool(len(job_settings))
    try:
        p.map(JobController.run, job_settings)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
