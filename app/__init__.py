from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Your config class

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Login view
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Please log in to access this page."

    # Blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()  # Ensure all tables are created during app initialization

    return app

from app.models import Users

@login_manager.user_loader
def load_user(user_id):
    try:
        # Query the database to get the user by ID
        user = db.session.query(Users).filter_by(user_ID=int(user_id)).first()
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

from app import routes