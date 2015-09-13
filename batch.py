#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

import logging
from multiprocessing import Pool
from xp2015_data_create import Xp2015DataCreate
from baseballdata_stats import BaseballdataStats
from strage_uploader import StorageUploader
from scheduler.job_controller import JobController


@JobController.run("10 22 * * *")
def baseballdata_create():
    """
    データで楽しむプロ野球からデータ出力
    :return:
    """
    logging.info("->- データで楽しむプロ野球 Create Start")
    # 実行モジュール
    cl = BaseballdataStats()
    uploader = StorageUploader()
    cl.dunn()
    logging.info("-<- データで楽しむプロ野球 Create Done.")
    logging.info("->- データで楽しむプロ野球 Upload Start")
    uploader.upload_files(
        cl.pitching_stats_service.output_path,
        cl.pitching_stats_service.extension,
        cl.pitching_stats_service.now_time
    )
    logging.info("-<- データで楽しむプロ野球 Upload Done.")

@JobController.run("00 22 * * *")
def xp2015_data_create():
    """
    XP祭り2015用データ作成
    :return:
    """
    logging.info("->- XP2015 Data Create Start")
    # 実行モジュール
    cl = Xp2015DataCreate()
    uploader = StorageUploader()
    cl.team_standings()
    cl.team_py_standings()
    cl.ops()
    cl.dunn()
    logging.info("-<- XP2015 Data Create Done.")
    logging.info("->- XP2015 Data Upload Start")
    uploader.upload_files(
        cl.standing_service.output_path,
        cl.standing_service.extension,
        cl.standing_service.now_time
    )
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
    jobs = [xp2015_data_create, baseballdata_create]

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
