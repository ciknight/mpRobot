# -*- coding: utf-8 -*-

import sae

from mp import app


application = sae.create_wsgi_app(app)
