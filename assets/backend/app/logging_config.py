import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # File handler
    file_handler = RotatingFileHandler(
        'logs/cryptex.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Cryptex startup')

def init_sentry(app):
    environment = app.config.get('ENV', 'development')
    sentry_sdk.init(
        dsn=app.config.get('SENTRY_DSN', ''),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment=environment
    ) 