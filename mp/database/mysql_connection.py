# -*- coding: utf-8 -*-

import pymysql

from .connection import Connection


class MySQLConnection(Connection):

    def __init__(self, **kwargs):
        super(MySQLConnection, self).__init__()
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 3306)
        self._user = kwargs.get('user')
        self._password = kwargs.get('password')
        self._db = kwargs.get('db')
        self._real_connect()

    def _real_connect(self):
        """ connection mysql use mysql derive """
        self._connection = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                db=self._db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
        self._connection.autocommit(1)

    def open(self):
        if self._connection is None:
            self._real_connect()

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def refresh(self):
        self.close()
        self.open()

    def get_connection(self):
        if self._connection is None:
            self._real_connect()
        self._connection.ping(reconnect=True)
        return self._connection
