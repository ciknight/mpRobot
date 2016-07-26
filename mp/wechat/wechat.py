# -*- coding: utf-8 -*-

import base64
import hashlib

from prpcrypt import Prpcrypt


class WeChat(object):

    def __init__(self, *args, **kwargs):
        super(WeChat, self).__init__()
        self.appid = kwargs.get('appid')
        self.token = kwargs.get('token')
        self.EncodingAESKey = kwargs.get('EncodingAESKey')
        assert self.token and self.appid
        self.key = base64.b64decode(self.EncodingAESKey + "=")
        if len(self.key) != 32:
            raise Exception('EncodingAESKey no valid')
        self.WXCrypt = Prpcrypt(self.key)

    def get_signature(self, timestamp=None, nonce=None, *args):
        sign = [self.token, timestamp, nonce] + list(args)
        sign.sort()
        sign = ''.join(sign)
        return hashlib.sha1(sign).hexdigest()

    def check_signature(self, signature, timestamp=None, nonce=None):
        sign = self.get_signature(timestamp, nonce)
        return sign == signature

    def decrypt_xml(self, encrypt, signature=None, timestamp=None, nonce=None):
        if not signature:
            raise TypeError('signature no valid')

        return self.WXCrypt.decrypt(encrypt, self.appid)
