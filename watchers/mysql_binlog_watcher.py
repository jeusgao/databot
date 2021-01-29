#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 22:56:33
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918

import os
import time
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

from utils import get_cfg, get_var, set_var, timestamp_maker

mysql_cfg = get_cfg('MYSQL_SOURCE')

dic_tables = mysql_cfg.get('TABLES')

except_fields = mysql_cfg.get('EXCEPT_FIELDS')
BINLOG_NUM_VAR = mysql_cfg.get('BINLOG_NUM_VAR')
LAST_TIMESTAMP_VAR = mysql_cfg.get('LAST_TIMESTAMP_VAR')

_log_path = mysql_cfg.get("LOG_PATH")
_log_pref = mysql_cfg.get("LOG_FILE_PREFIX")

fpath_log_index = f'{_log_path}/{_log_pref}.index'
fpath_log_latest = None
if os.path.exists(fpath_log_index):
    with open(fpath_log_index, 'r') as f:
        lines = f.read().splitlines()
    if len(lines) == 1:
        fpath_log_latest = lines[0]
    elif len(lines) > 1:
        fpath_log_latest = lines[-2]
else:
    fpath_log_latest = f'{_log_path}/{_log_pref}.000001'

timestamp = get_var(mysql_cfg.get('LAST_TIMESTAMP_VAR'))
if timestamp:
    timestamp = int(timestamp) + 1
else:
    timestamp = timestamp_maker(mysql_cfg.get('INIT_TIME'))

stream = BinLogStreamReader(
    connection_settings=mysql_cfg.get('CONN_SETTINGS'),
    server_id=mysql_cfg.get('SERVER_ID'),
    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
    resume_stream=True,
    blocking=True,
    log_file=fpath_log_latest,
    log_pos=4,
    only_tables=list(dic_tables.keys()),
    only_schemas=mysql_cfg.get('DBNAMES'),
    freeze_schema=True,
    skip_to_timestamp=timestamp,
    slave_heartbeat=10,
)


def mysql_watcher():
    for binlogevent in stream:
        logs = []
        for row in binlogevent.rows:
            _tmp = {}
            if isinstance(binlogevent, DeleteRowsEvent):
                _tmp = {'action': 'delete'}
            elif isinstance(binlogevent, UpdateRowsEvent):
                _tmp = {'action': 'update'}
            elif isinstance(binlogevent, WriteRowsEvent):
                _tmp = {'action': 'insert'}

            _tmp['row'] = row
            _tmp['table'] = binlogevent.table
            _tmp['ts'] = binlogevent.timestamp

            logs.append(_tmp)

        set_var(LAST_TIMESTAMP_VAR, binlogevent.timestamp)
        stream.close()

        if logs:
            yield logs, except_fields, dic_tables
