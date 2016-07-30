# -*- coding: utf8 -*-


class DatabaseNotFoundException(Exception):
    pass


class Connection(object):
    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()
