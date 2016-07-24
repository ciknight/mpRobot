# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

app.route('/confim')
def confim():
    return 'Hello Wrold'
