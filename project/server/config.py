# server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig():
    """Development configuration."""
    DEBUG = True
    SECRET_KEY = "this_secret"
