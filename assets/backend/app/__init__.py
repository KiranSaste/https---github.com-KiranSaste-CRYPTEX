from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from .config import Config # Import the Config class from config
# app = create_app()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Redirects unauthorized users to the login page

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) #This tells Flask to import the Config class from config.py.
    
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app) # Initialize CSRF protection
    
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()


# Import routes inside the function to avoid circular imports
    # from app import routes  # Import routes after initializing Flask app
    from app.routes import main
    app.register_blueprint(main)

    return app






