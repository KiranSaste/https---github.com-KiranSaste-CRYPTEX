import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Admin@123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:Admin2025@localhost:3306/cryptex')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    TESTING = False
    # You can learn more about configuring Flask with SQLAlchemy from this YouTube video:
    # https://www.youtube.com/watch?v=cYWiDiIUxQc

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False











