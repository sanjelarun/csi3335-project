# __init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from flask_login import LoginManager

login = LoginManager(app)
login.login_view = 'login'

from app import routes
