# -*- coding: UTF-8 -*-
"""
Created on 2016/6/2

@author: mavericks
"""

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = 'test_db'


class TestingConfig(Config):
    TESTING = True
    MONGO_DBNAME = 'test_db'


class Production(Config):
    DEBUG=True
    MONGO_DBNAME = 'test_db'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}