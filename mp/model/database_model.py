# -*- coding: utf-8 -*-

from mp.config import Config
from mp.database import MySQLConnection, MySQLPool


class DataBaseModel(object):
    # _POOL = MySQLPool(Config.MYSQL.get('pool_size'), **Config.MYSQL.get('config')).pool

    def save(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    @classmethod
    def get_connection(cls):
        # TODO <ci_knight> MySQL Pool
        return MySQLConnection(**Config.MYSQL.get('config')).get_connection()

    @classmethod
    def open(self):
        return

    @classmethod
    def factory(cls, attrs):
        if attrs is None: return None
        return cls(**attrs)
