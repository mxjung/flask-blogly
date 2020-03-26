"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime
# from sqlalchemy import DateTime

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
    # get or 404

    user.first_name = first_name
    user.last_name = last_name

    if not image_url:
        image_url = 'https://i.imgur.com/XVicMmG.jpg'

    user.image_url = image_url

    db.session.commit()


def delete_user(id):
    "delete a user and commit to DB"

    user = User.query.get_or_404(int(id))
    # filter(User.id == int(user_id)) # this doesn't work

    db.session.delete(user)
    db.session.commit()


class User(db.Model):
    '''User'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default='https://i.imgur.com/XVicMmG.jpg')

    # posts = db.relationship('Post', backref='users')


class Post(db.Model):
    '''Posts'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('User')
