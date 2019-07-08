# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 10:50
# @Author  : Li Fu

import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
envdir = os.path.abspath(os.path.join(basedir, '../env.json'))

with open(envdir) as file:
    env_json_str = file.read()
    env = json.loads(env_json_str)


class Config:
    SECRET_KEY = env['SECRET_KEY'] or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <%s>' % (env['FLASKY_ADMIN'])
    FLASKY_ADMIN = env['FLASKY_ADMIN']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = env['MAIL_SERVER']
    MAIL_USERNAME = env['MAIL_USERNAME']
    MAIL_PASSWORD = env['MAIL_PASSWORD']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
