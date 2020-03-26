"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, add_user, update_user, delete_user
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()
debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    "index page, redirects to '/users'"
    return redirect('/users')


@app.route('/users')
def user_listing():
    "Show list of all users"

    users = User.query.all()

    return render_template('user-listing.html', title='Users', users=users)


@app.route('/users/new')
def create_user():
    "Create a new user"
    return render_template('new-user-form.html', title="Create a User")


@app.route('/users/new', methods=["POST"])
def store_new_user():
    "Accepts POST request of new user"

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    add_user(first_name, last_name, image_url)

    flash(f"{first_name} {last_name} was added as a user.")
    return redirect('/users')


@app.route('/users/<user_id>')
def show_user(user_id):
    "generate user detail page"

    user = User.query.filter(User.id == int(user_id)).one()
    # get_or_404 (user here)

    return render_template('user-detail-page.html',
                           title=f"{user.first_name} {user.last_name}",
                           user=user)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):

    user = User.query.filter(User.id == int(user_id)).one()
    # get_or_404 (user here)

    return render_template('user-edit.html',
                           title=f"{user.first_name} {user.last_name}",
                           user=user)


@app.route('/users/<user_id>/edit', methods=['POST'])
def store_edits(user_id):

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    update_user(user_id, first_name, last_name, image_url)

    flash(f"{first_name} {last_name} information updated.")
    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    "Delete the user"
    # delete_user(user_id)

    user = User.query.get_or_404(int(user_id))
    # filter(User.id == int(user_id)) # this doesn't work
    
    db.session.delete(user)
    db.session.commit()

    flash("User deleted.")
    return redirect('/users')
