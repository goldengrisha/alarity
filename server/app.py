import nltk
from os import environ
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI


# Download punkt for proper sentence separating.
nltk.download('punkt')

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

with app.app_context():
    import routes
    # Create database tables for our data models
    db.create_all()


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
