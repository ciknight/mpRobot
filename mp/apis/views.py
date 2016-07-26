# -*- coding: utf-8 -*-

from flask import abort, request, g

from mp.wechat import wechat
from mo.wechat import MPMessageModel
from . import api_blueprint


@api_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    try:
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')  # 随机数
        assert wechat.check_signature(signature, timestamp, nonce)
    except:
        g.logger.error('signature no valid')
        return abort(403)

    if request.methods == 'GET':
        return request.args.get('echostr')

    elif request.methods == 'POST':
        post_data = request.data
        if 'Encrypt' in post_data:
            xml_content = wechat.decrypt_xml(post_data,
                    signature=signature,
                    timestamp=timestamp,
                    nonce=nonce)
        else:
            xml_content = post_data

        data = MPMessageModel.parser(xml_content)
    return 'Hello Python2!'
