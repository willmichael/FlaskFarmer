# server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig():
    """Development configuration."""
    DEBUG = True
    SECRET_KEY = "this_secret"
    MONGO_DBNAME = "test_collection"
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class TestingConfig():
    """Testing configuration."""
    DEBUG = True
    SECRET_KEY = "this_secret"
    MONGO_DBNAME = "testing_config"
