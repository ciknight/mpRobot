# -*- coding: utf-8 -*-

from flask import request
from . import wechat


class Decorators(object):

    def before_confirm(self):
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')  # 随机数
        signature = request.args.get('signature', '')
        assert wechat.check_signature(timestamp, nonce, signature)
