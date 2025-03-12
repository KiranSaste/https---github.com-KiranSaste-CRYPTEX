from app import create_app, db

# app = create_app()

from assets.backend.app import create_app

app = create_app()  # Initialize the Flask app

with app.app_context():  # Activate the application context
    db.create_all()  # Create tables


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy # for fetching th data
from flask_migrate import Migrate
from backend.app.config import Config

app = Flask(__name__)

app.config.from_object(Config)  # fetching database URI from file configdb
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)