# project/server/__init__.py

import os
import logging
logging.basicConfig(filename='test.log',level=logging.DEBUG)

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('server.config.DevelopmentConfig')

mongo = PyMongo(app)
auth = HTTPBasicAuth()

import server.api.views
import server.auth.views

# establish userid counter
with app.app_context():
    counter_exists = mongo.db.counters.find_one()
    if counter_exists == None:
        mongo.db.counters.insert(
            {
                "_id": "userid",
                "seq": 0
            }
        )




