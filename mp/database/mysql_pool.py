# -*- coding: utf-8 -*-

import pymysql
from DBUtils import PersistentDB

from mp.util import MetaSingleton

class MySQLPool(object):
    __metaclass__ = MetaSingleton

    def __init__(self, pool_size, **kwargs):
        self._pool_size = pool_size
        self._pooled = PersistentDB(pymysql, pool_size, **kwargs)

    def get_db(self):
        return self._pooled.connection()

    def pool_size(self):
        return self._pool_size
