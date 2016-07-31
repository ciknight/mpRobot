# -*- coding: utf-8 -*-

from flask import abort, request, g

from mp.wechat import wechat
from mp.wechat import MPMessageModel
from mp.robot import robot
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
        try:
            echostr = request.args.get['echostr']
        except Exception as e:
            g.logger.error('request parm is not echostr!')
            return abort(403)

        return echostr

    elif request.methods == 'POST':
        post_data = request.data
        if 'Encrypt' in post_data:
            try:
                xml_content = wechat.decrypt_xml(post_data,
                        signature=signature,
                        timestamp=timestamp,
                        nonce=nonce)
            except Exception as e:
                g.logger.error(str(e))
                return abort(403)
        else:
            xml_content = post_data

        message = MPMessageModel.parser(xml_content)
        try:
            message.replay = robot.replay(message)
        except Exception as e:
            g.logger.error(str(e))

        return  message.to_xml()

    return 'Hello Python2!'
