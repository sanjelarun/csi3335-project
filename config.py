# config.py

import os
from app.csi3335F23 import mysql

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['host']}/{mysql['db']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
