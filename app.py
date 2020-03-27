"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, add_user, update_user, delete_user, submit_post, edit_submit_post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()
debug = DebugToolbarExtension(app)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


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
                           user=user, posts=user.posts)


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


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    "create a new post for a user"

    user = User.query.get_or_404(int(user_id))

    return render_template('new-post-form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def store_post(user_id):
    "submit post"

    title = request.form['title']
    content = request.form['content']

    submit_post(user_id, title, content)

    flash(f"{title} post submitted.")
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    "displays a specific post"

    post = Post.query.get(post_id)

    return render_template('post-detail-page.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    "edit a post"

    post = Post.query.get(post_id)

    return render_template('post-edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit_post(post_id):
    "submit edited post to DB"

    title = request.form['title']
    content = request.form['content']

    edit_submit_post(post_id, title, content)

    flash(f"{title} post edited.")
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    "delete post from DB"

    post = Post.query.get(post_id)
    old_post = post.users.id

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted.")
    return redirect(f'/users/{old_post}')
