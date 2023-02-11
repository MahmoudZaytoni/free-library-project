from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password = db.Column(db.String(100), nullable=False)
  added_date = db.Column(db.DateTime(), default=datetime.utcnow)

  def __repr__(self):
    return f'<Name {self.first_name}>'

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  author = db.Column(db.String(50), nullable=False)
