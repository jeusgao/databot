#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 22:56:33
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918

import os
import time
from multiprocessing.dummy import Pool
# from celery.states import state, PENDING, SUCCESS, FAILURE
from tasks import mysql_excute
from watchers import mysql_watcher
from fetchers import mysql_fetcher
from utils import mysql_build_sql
import jobot_logger

logger = jobot_logger.get_logger(logger_name='Watcher')
logger.info(f'MySQL Watcher: Start watching ...')


def _map(param):
    log, except_fields = param
    record = mysql_fetcher.main(log.get('action'), log.get('row'), except_fields)

    if record.get('flag'):

        logger.info(f"MySQL Fetcher: {log.get('action')} {log.get('table')}")

        _sql = mysql_build_sql(
            log.get('action'),
            log.get('table'),
            record.get('values'),
            record.get('diff_values'),
            dic_tables,
        )
        if len(_sql):
            logger.info(f'MySQL Excutor: Excuting SQL: \n\t {_sql}')
            res = mysql_excute.delay(_sql)
            logger.info(f'MySQL Excutor({res.id}): {res.state}')

while True:
    logs, except_fields, dic_tables = next(mysql_watcher())

    pool = Pool(8)
    pool.map(_map, [(l, except_fields) for l in logs])
    pool.close()
    pool.join()
