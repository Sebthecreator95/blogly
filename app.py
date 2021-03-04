"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
def home_page():
    """Show Home Page"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('home.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Show a form to create a new user"""

    return render_template('newUserForm.html')


@app.route("/users/new", methods=["POST"])
def new_user():
    """Handle form submission for creating a new user"""

    new_user = User(first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        username = request.form['username'],
        image_url = request.form['image_url'] or 'https://image.shutterstock.com/image-vector/no-user-profile-picture-hand-260nw-99335579.jpg')
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show a page with info on a specific user that was clicked on"""
    user = User.query.get_or_404(user_id)
    return render_template('showUser.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit_page(user_id):
    """Show a form to edit an existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('usersEditPage.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.username = request.form['username']

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")