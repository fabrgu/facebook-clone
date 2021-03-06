import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize app
app = Flask(__name__)


# db/app configuration functions
def get_connection_string():
    if 'DATABASE_URL' in os.environ:
        return os.environ['DATABASE_URL']
    else:
        return 'postgresql:///facebook-clone'

def configure_db(app):
    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # uncomment to see sql for debugging 
    # app.config['SQLALCHEMY_ECHO'] = True

def configure_app(app):
    app.secret_key = "ABC"
    # uncomment to set to debug
    # app.debug = True
    # app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

configure_app(app)
configure_db(app)


# Instantiate a SQLAlchemy object. We need this to create our db.Model classes.
db = SQLAlchemy(app)


# initalize db function
def connect_to_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)

connect_to_db(app)