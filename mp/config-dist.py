# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False

    WECHAT = {
        'appid': '',
        'secret': '',
        'token': '',
        'EncodingAESKey': ''
    }

    _MYSQL_CONFIG = dict(
        host='x.x.x.x',
        port=3306,
        user='xxx',
        password='xxx',
        db='app')

    MYSQL = {
        'config': _MYSQL_CONFIG,
        'pool_size': 2
    }

    TULING = {
        'key': '',
        'secret': ''
    }
