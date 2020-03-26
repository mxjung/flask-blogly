"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


def add_user(first_name, last_name, image_url):
    "collects new user, adds it to session, and commits to DB"

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url)

    if not user.image_url:
        user.image_url = None

    db.session.add(user)
    db.session.commit()


def update_user(id, first_name, last_name, image_url):
    "collects updated user info and commits to DB"

    user = User.query.filter(User.id == int(id)).one()

    user.first_name = first_name
    user.last_name = last_name

    if not image_url:
        image_url = 'https://i.imgur.com/XVicMmG.jpg'

    user.image_url = image_url

    db.session.commit()


def delete_user(id):
    "delete a user and commit to DB"

    User.query.filter(User.id == id).delete()

    db.session.commit()


class User(db.Model):
    '''User'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default='https://i.imgur.com/XVicMmG.jpg')
