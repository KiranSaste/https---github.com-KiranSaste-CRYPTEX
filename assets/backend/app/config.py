import os

class Config:
    SECRET_KEY = 'Admin@123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Admin2025@localhost:3306/cryptex'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You can learn more about configuring Flask with SQLAlchemy from this YouTube video:
    # https://www.youtube.com/watch?v=cYWiDiIUxQc
