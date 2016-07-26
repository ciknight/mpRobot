# -*- coding: utf-8 -*-

import logging

from flask import Flask, g

from mp.apis import api_blueprint
from mp.config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(api_blueprint)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(app.debug and logging.DEBUG or logging.INFO)

@app.before_request
def before_request():
    g.logger = app.logger
