# -*- coding: utf-8 -*-

from flask import request

from . import api_blueprint


@api_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    return 'Hello world'
