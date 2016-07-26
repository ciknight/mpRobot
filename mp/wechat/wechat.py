# -*- coding: utf-8 -*-

import hashlib


class WeChat(object):

    def __init__(self, *args, **kwargs):
        super(WeChat, self).__init__()
        self.token = kwargs.get('token')
        assert self.token

    def get_signature(self, timestamp=None, nonce=None, *args):
        sign = [self.token, timestamp, nonce] + list(args)
        sign.sort()
        sign = ''.join(sign)
        return hashlib.sha1(sign).hexdigest()

    def check_signature(self, signature, timestamp=None, nonce=None):
        sign = self.get_signature(timestamp, nonce)
        return sign == signature
