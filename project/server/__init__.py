# project/server/__init__.py

import os
import logging
logging.basicConfig(filename='test.log',level=logging.DEBUG)

from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

import server.api.views
import server.auth.views

app.config.from_object('server.config.DevelopmentConfig')

def authorize(f):
    @wraps(f)
    def decorate_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        user = None

        return f(user, *args, **kws)
    return decorate_function



