"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)    
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')

