# server/tests/base.py

from flask_testing import TestCase
from flask import Flask

from server import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('project.server.config.DevelopmentConfig')
        return app

