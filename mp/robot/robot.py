# -*- coding: utf-8 -*-

import time

from mp.config import Config
from mp.model import MessageModel
from mp.wechat import session
from mp.util import MetaSingleton
from .tuling import TuLing
from .auth import Auth


class Robot(object):
    __metacalss__ = MetaSingleton

    def __init__(self):
        self.cli = {}
        self.auth = Auth()
        self.tuling = TuLing(api_key=Config.TULING.get('key'),
                api_secret=Config.TULING.get('secret'))
        self.init_cli()

    def _set_lastRecv(self, user):
        if not session.get_user(user.wechat):
            session.save_user(user.wechat)

        session.update_user(user.id, 'lastRecv', int(time.time()))

    def _register_cli(self, cmd, func):
        if self.cli.get(cmd):
            raise Exception, 'repeat cmd'

        self.cli[str(cmd)] = func

    def init_cli(self):
        self._register_cli('lastRecv', self._set_lastRecv)

    def replay(self, message):
        user = self.auth.get_user(message.from_id)
        if not user:
            if self.auth.reg_cmd in message.message:
                username = self.auth.parse_username(message.message)
                return self.auth.register_user(message.from_id, username)
            return u'请发送我叫XXX进行注册，即可解锁更多功能。'

        for cmd, func in self.cli.items():
            if cmd in message.message:
                return func(user)

        replay_text = self.tuling.replay_text(message.message)
        m = MessageModel()
        m.content = message.message
        m.replay = replay_text
        m.wechat_id = message.from_id
        m.user_id = user.id
        m.save()
        return replay_text
