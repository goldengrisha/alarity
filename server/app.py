from os import environ
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create database tables for our data models

        return app


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    create_app().run(HOST, PORT)
