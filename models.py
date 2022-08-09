"""SQLAlchemy models for Capstone One."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true

bcrypt = Bcrypt()
db = SQLAlchemy()


class Users(db.Model):
  """will be the model for users"""
  
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(250), nullable=False)
  watched = db.relationship('Watched', backref='users',lazy=True)
  transactions = db.relationship('Transactions',backref='users', lazy=True)
    # addresses = db.relationship('Address', backref='person', lazy=True)
  
  def __repr__(self):
    return '<User %r>' % self.username

class Watched(db.Model):
  """ The members of congress that you want to watch"""
  
  __tablename__ = 'watched'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80),nullable=False)
  user_id = db.Column(db.Integer ,db.ForeignKey('users.id'),nullable=False)

  def __repr__(self):
    return '<watched %r>' % self.name

class Transactions(db.Model):
  """ Specific transactions a user wants to track. Will relate to a Watched memeber"""
  
  __tablename__ = 'transactions'
  
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String, nullable=False)
  info = db.Column(db.String(500))
  company = db.Column(db.String(120))
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)