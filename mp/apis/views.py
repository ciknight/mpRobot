# -*- coding: utf-8 -*-

from flask import request, g

from mp.wechat import wechat
from . import api_blueprint


@api_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    try:
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')  # 随机数
        signature = request.args.get('signature')
        assert wechat.check_signature(signature, timestamp, nonce)
    except:
        g.logger.error('signature no valid')
        return None

    if request.methods == 'GET':
        return request.args.get('echostr')
    return 'Hello world'
