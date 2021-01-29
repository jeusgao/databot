#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-08 14:53:24
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import logging


def get_logger(logger_name='RESTFUL'):
    fh = logging.FileHandler('logs/runtime.log', encoding='utf-8')  # 创建一个文件流并设置编码utf8
    ch = logging.StreamHandler()  # 日志输出到屏幕控制台

    logger = logging.getLogger(logger_name)  # 获得一个logger对象，默认是root
    logger.setLevel(logging.INFO)  # 设置最低等级debug

    # fh.setLevel(logging.DEBUG)
    # ch.setLevel(logging.INFO)

    fm = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # 设置日志格式

    logger.addHandler(fh)  # 把文件流添加进来，流向写入到文件
    logger.addHandler(ch)  # screen show

    fh.setFormatter(fm)  # 把文件流添加写入格式
    ch.setFormatter(fm)

    return logger
