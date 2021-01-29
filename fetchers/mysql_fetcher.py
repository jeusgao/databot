#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 22:56:33
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918

import os
from utils import dict_pop


def main(action, row, except_fields):

    prev_vals, vals, diff_vals, flag = None, None, None, False

    if action in ['delete', 'insert']:
        prev_vals = None
        vals = row["values"]
        flag = True

    elif 'update' in action:
        prev_vals = row["before_values"]
        vals = row["after_values"]

        _diff = prev_vals.keys() & vals
        if _diff:
            diff_vals = {k: vals.get(k) for k in _diff if prev_vals[k] != vals[k]}
            prev_vals = dict_pop(except_fields, diff_vals)
            flag = True if len(diff_vals) else False

    return {
        'prev_values': prev_vals,
        'values': vals,
        'diff_values': diff_vals,
        'flag': flag,
    }
