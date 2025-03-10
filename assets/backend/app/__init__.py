from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import Config

# from app import create_app, db

# app = create_app()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirects unauthorized users to the login page

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) #This tells Flask to import the Config class from config.py.
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)

    # with app.app_context():
    #     from app import routes

# Import routes inside the function to avoid circular imports
    from app import routes  # Import routes after initializing Flask app
    from app.routes import main
    app.register_blueprint(main)

    return app
