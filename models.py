"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    @property
    def full_name(self):
        """Get Full Name"""
        return f"{self.first_name} {self.last_name}"
    def __repr__(self):
        u = self
        return f'<User id={u.id} username={u.username} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    username = db.Column(db.String(30),nullable= False, unique= True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30),nullable = False)
    image_url = db.Column(db.Text, default='https://image.shutterstock.com/image-vector/no-user-profile-picture-hand-260nw-99335579.jpg')