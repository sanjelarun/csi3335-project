from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#import mariadb
import pymysql
import sys
import app.csi3335F23 as myDb


app = Flask(__name__)
'''app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)'''
# if using pymysql:
conn = pymysql.connect(
         host=myDb.mysql['host'],
         user=myDb.mysql['user'],
         password=myDb.mysql['password'],
         db=myDb.mysql['db'])
cursor = conn.cursor()

#if using mariadb (WE ARE NOT)
# conn = mariadb.connect(
#     host = '127.0.0.1',
#     port = 3306,
#     user = 'root',
#     password = '',
#     database = 'baseball'
# )

cursor = conn.cursor()

login = LoginManager(app)
login.login_view = 'login'

from app import routes