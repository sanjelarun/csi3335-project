import os

from csi3335f2024 import mysql

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'itsPartyTimeWhoopWhoop'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    f'mysql+pymysql://{mysql["user"]}:{mysql["password"]}@{mysql["location"]}:3306/{mysql["database"]}'



