# -*- coding: utf-8 -*-

from flask import abort, request, g

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
        return abort(403)

    if request.methods == 'GET':
        return request.args.get('echostr')

    elif request.methods == 'POST':
        post_data = request.data
        if 'Encrypt' in post_data:
            xml_content = None
        else:
            xml_content = post_data

    return 'Hello Python2!'
