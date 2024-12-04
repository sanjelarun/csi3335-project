from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'

    # Import and register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Define user_loader here to avoid circular imports
    from app.models import Users

    @login.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))  # Return the user object from the database

    return app