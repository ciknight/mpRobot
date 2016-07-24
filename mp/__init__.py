# -*- coding: utf-8 -*-

from flask import Flask

from mp.config import Config

app = Flask(__name__)

app.config.from_object(Config)

app.route('/confirm')
def confim():
    return 'Hello Wrold'
