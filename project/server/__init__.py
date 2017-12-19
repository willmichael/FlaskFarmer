# project/server/__init__.py

import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

import server.api.views
import server.auth.views


