# -*- coding: utf-8 -*-

from .auth import Auth


class Robot(object):

    def __init__(self):
        self.cli = {}
        self.auth = Auth()
        self.register_cli(
                self.auth.reg_cli,
                self.auth.register_user)

    def register_cli(self, cli, func):
        cli = str('cli')
        self.cli[cli] = func

    def _robot(self):
        pass

    def replay(self, message):
        user = self.auth.get_user(message.from_id)
        if not user:
            if '我叫' in message.message:
                username = self.auth.parse_username(message.message)
                return self.cli[self.auth.reg_cli](message.from_id, username)
            return '请发送我叫XXX进行注册，以便获得更多服务。'

        for cli, func in self.cli.items():
            if cli in message.message:
                return func(user)

        return 'hello, System Development!'
