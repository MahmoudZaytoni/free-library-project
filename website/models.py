from .extensions import db
from datetime import datetime
from flask_login import UserMixin

favorite = db.Table('favorite', 
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password = db.Column(db.String(100), nullable=False)
  added_date = db.Column(db.DateTime(), default=datetime.utcnow)
  favor = db.relationship('Book', secondary=favorite, backref='favorites')

  def __repr__(self):
    return f'<Name {self.first_name}>'

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  author = db.Column(db.String(50), nullable=False)
  cover = db.Column(db.String(50), nullable=False)
  file_name = db.Column(db.String(50), nullable=False)
  desc = db.Column(db.String(1000), nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

  def __repr__(self):
    return f'<Book: {self.title}>'

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_name = db.Column(db.String(50), nullable=False)
  books = db.relationship('Book', backref="category")

  def __repr__(self):
    return f'<Category: {self.category_name}>'