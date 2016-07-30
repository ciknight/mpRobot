# -*- coding: utf-8 -*-

from flask import Blueprint

api_blueprint = Blueprint('api',
        __name__,
        template_folder='templates')

from . import views
