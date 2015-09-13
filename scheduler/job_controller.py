#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import time
import functools
import logging
from crontab import CronTab
from scheduler.job_settings import JobSettings


class JobController(object):
    """
    ジョブ実行Controller
    """

    @classmethod
    def run(cls, crontab):
        """
        処理実行
        :param crontab: job schedule
        """
        def receive_func(job):
            @functools.wraps(job)
            def wrapper():

                job_settings = JobSettings(CronTab(crontab))
                logging.info("->- Process Start")
                while True:
                    try:
                        logging.info(
                            "-?- next running\tschedule:%s" %
                            job_settings.schedule().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        time.sleep(job_settings.interval())
                        logging.info("->- Job Start")
                        job()
                        logging.info("-<- Job Done")
                    except KeyboardInterrupt:
                        break
                logging.info("-<- Process Done.")
            return wrapper
        return receive_func
