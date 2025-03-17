from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from .config import Config # Import the Config class from config
# app = create_app()

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Redirects unauthorized users to the login page

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) #This tells Flask to import the Config class from config.py.
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # Import routes inside the function to avoid circular imports
    from app.routes import main, trading, crypto_api
    app.register_blueprint(main)
    app.register_blueprint(trading)
    app.register_blueprint(crypto_api)
    
    # Register error handlers
    from app.error_handlers import errors
    app.register_blueprint(errors)
    
    # Initialize logging
    from app.logging_config import setup_logging, init_sentry
    setup_logging(app)
    if not app.config.get('TESTING', False):
        init_sentry(app)
    
    # Initialize caching and rate limiting with error handling
    try:
        from app.cache import cache, limiter
        cache.init_app(app)
        limiter.init_app(app)
        app.logger.info("Cache and rate limiter initialized successfully")
    except Exception as e:
        app.logger.warning(f"Error initializing cache/limiter: {str(e)}")
        app.logger.info("Application will run without caching and rate limiting")

    return app






