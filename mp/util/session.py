# -*- coding: utf-8 -*-

import time


class Session(object):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__()
        self._session = dict()

    def save(self, key, value=int(time.time())):
        self._session[key] = value
        return self

    def get(self, key, default=None):
        return self._session.get(key, default)

    def update(self, key, value=int(time.time())):
        self._session.update(key, value)
        return self

    def delete(self, key):
        if self.get(key):
            del self._session[key]
        return self

    def clear(self):
        self._session.clear()
        return self
