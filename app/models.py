# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import sessionmaker
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from hashlib import md5
# from datetime import datetime, timezone
#
# # Define your database connection URL
# database_url = 'your_database_connection_url'
#
# # Create an SQLAlchemy engine
# engine = create_engine(database_url)
#
# # Reflect the existing tables from the database
# Base = automap_base()
# Base.prepare(engine, reflect=True)
#
# # Access the reflected tables
# User = Base.classes.user
# Team = Base.classes.teams
# Batting = Base.classes.batting
# RequestLog = Base.classes.request_log
#
# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()
#
#
# # Define UserMixin and additional methods
# class UserMixinExtended(UserMixin):
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def avatar(self, size):
#         digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#         return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
#
#
# # Extend User class with UserMixinExtended
# class User(UserMixinExtended):
#     pass
#
#
# # Define additional methods or properties for other classes if needed
#
#
# # Define metadata and create a session
# metadata = MetaData(bind=engine)
# Base.prepare(engine, reflect=True)



from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    favorite_team: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), nullable=True)
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class RequestLog(db.Model):
    __tablename__ = 'request_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    request_data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<RequestLog id={self.id}, user_id={self.user_id}, timestamp={self.timestamp}>"