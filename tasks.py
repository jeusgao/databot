#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-13 14:51:55
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import os
from celery import Celery

from excutors import MySQLExcutor
from utils import get_cfg

mysql_cfgs = get_cfg('MYSQL_TARGET')

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis',
)
mysqlexcutor = MySQLExcutor()


@app.task
def mysql_excute(sql):
    for cfg in mysql_cfgs:
        dbs = cfg.get('DBS')
        for db in dbs:
            mysqlexcutor.get_conn(db, **cfg)
            mysqlexcutor.excute(sql)
