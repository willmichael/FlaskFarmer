# server/tests/base.py

from flask_testing import TestCase
from flask import Flask

from server import app, mongo


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        counter_exists = mongo.db.counters.find_one()
        if counter_exists == None:
            mongo.db.counters.insert(
                {
                    "_id": "userid",
                    "seq": 0
                }
            )

    def tearDown(self):
        mongo.db.users.drop()
        mongo.db.counters.drop()
