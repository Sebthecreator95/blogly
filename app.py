"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'TopSecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug =DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def posts():
    """Show a list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('posts.html', posts=posts)

@app.route('/users')
def users():
    """Show Users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('users.html', users=users)

@app.route('/new-users', methods=['GET'])
def new_user_form():
    """Show a form to create a new user"""
    return render_template('newUserForm.html')


@app.route('/new-users' methods=['POST'])
def new_user_submit():
    """Handle form submission for creating a new user"""

    new_user = User(first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        username = request.form['username'],
        image_url = request.form['image_url'] or 'https://image.shutterstock.com/image-vector/no-user-profile-picture-hand-260nw-99335579.jpg')
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<string:username>')
def show_user(username):
    """Show a page with info on a specific user that was clicked on"""
    user = User.query.get_or_404(username)

    return render_template('showUser.html', user=user)


@app.route('/users/<string:username>/edit')
def users_edit_page(username):
    """Show a form to edit an existing user"""
    user = User.query.get_or_404(username)

    return render_template('usersEditPage.html', user=user)


@app.route('/users/<string:username>/edit', methods=['POST'])
def user_update(username):
    """updating an existing user"""

    user = User.query.get_or_404(username)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.username = request.form['username']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<string:username>/delete', methods=['POST'])
def user_delete(username):
    """deleting an existing user"""
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

    @app.route('/users/<string:username>/new-post')
def new_post_form(username):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(username)
    return render_template('userNewPost.html', user=user)


@app.route('/users/<string:username>/new-post', methods=['POST'])
def new_post_submit(username):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(username)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post.title}" added.')

    return redirect(f'/users/{username}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('showPost.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('editUserPost.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.username}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f'/users/{post.username}')