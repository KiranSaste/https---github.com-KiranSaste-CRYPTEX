# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from configdb import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)