# -*- coding: utf-8 -*-

from mp.util import Session, MetaSingleton


class WeChatSession(object):
    __metacalss__ = MetaSingleton

    def __init__(self, *args, **kwargs):
        super(WeChatSession, self).__init__()
        self._session = Session()

    @property
    def session(self):
        return self._session

    def get_user(self, from_id, default=dict()):
        return self.session.get(from_id, default)

    def save_user(self, from_id):
        self.session.save(from_id, dict())
        return self

    def update_user(self, from_id, key, value):
        if not self.session.get(from_id):
            return None

        self.session.get(from_id)[key] = value
        return self
