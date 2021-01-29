#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-20 22:41:00
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

from ZODB import DB
from ZODB.FileStorage import FileStorage
from ZODB.PersistentMapping import PersistentMapping
from Persistence import Persistent
import transaction

storage = FileStorage("db/mysql.fs")
db_mysql = DB(storage)
