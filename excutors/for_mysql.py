#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 22:43:41
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import pymysql


class MySQLExcutor(object):

    def __init__(self):
        self.connection = None

    def get_conn(self, db, **kwargs):
        self.connection = pymysql.connect(
            host=kwargs.get('HOST'),
            port=kwargs.get('PORT'),
            user=kwargs.get('USER'),
            password=kwargs.get('PASSWORD'),
            db=db,
            charset='utf8',
        )

    def excute(self, sql):
        self.connection.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()

        finally:
            self.connection.close()
