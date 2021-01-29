#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 17:59:22
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import os
import time
import json


def timestamp_maker(t):
    if isinstance(t, str):
        return time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S:%f'))
    else:
        return time.mktime(t)


def get_cfg(key):
    with open('config.json', 'r') as f:
        cfg = json.load(f)
    return cfg.get(key)


def dict_pop(keys, dic):
    for key in keys:
        if key in dic:
            dic.pop(key)
    return dic


def set_var(filename, value):
    if not isinstance(value, str):
        value = str(value)
    with open(filename, 'w') as f:
        f.write(value)


def get_var(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            var = f.read().splitlines()
        if len(var):
            return var[0]
        else:
            return None
    else:
        return None


def mysql_build_sql(action, table, vals, diff_vals, dic_tables):
    _pk = dic_tables.get(table)
    _pk_value = vals.get(_pk)
    _pk_value = f"'{_pk_value}'" if isinstance(_pk_value, str) else _pk_value

    def _modify_sql(vals):
        keys = [f'`{k}`' for k in vals.keys()]
        values = [f"'{v}'" if isinstance(v, str) else f'{v}' for v in vals.values()]
        return keys, values

    sql = ''

    if action in ['delete']:
        pass
        # sql = f"delete from {table} where `{_pk}`={_pk_value}"

    elif action in ['insert']:
        keys, values = _modify_sql(vals)
        sql = f"insert into {table} ({','.join(keys)}) values ({','.join(values)})"

    elif action in ['update']:
        keys, values = _modify_sql(diff_vals)
        _sub = ','.join([f'{k}={v}' for k, v in zip(keys, values)])
        sql = f"update {table} set {_sub} where `{_pk}`={_pk_value}"

    return sql
