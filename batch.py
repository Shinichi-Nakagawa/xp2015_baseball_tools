#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import logging
from multiprocessing import Pool
from xp2015_data_create import Xp2015DataCreate
from scheduler.job_controller import JobController


@JobController.run("17 01 * * *")
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
    jobs = [xp2015_data_create, ]

    # multi process running
    p = Pool(len(jobs))
    try:
        for job in jobs:
            p.apply_async(job)
        p.close()
        p.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
