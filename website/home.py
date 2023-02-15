from flask import Blueprint, render_template, redirect, flash, url_for, send_file, request
from flask_login import current_user, login_required
from .models import Book, Category
from . import db

home = Blueprint('home', __name__)

@home.route("/", methods=["GET", "POST"])
@login_required
def index():
  categories = Category.query.all()
  if 'search' in request.form:
    search = request.form.get('search')
    books = Book.query.filter(Book.title.like(f"%{search}%")).all()
  else:
    books = Book.query.all()
  return render_template("home.html", current_user=current_user, books=books, categories=categories)

@home.route("/tag/<int:id>", methods=["GET", "POST"])
@login_required
def filter(id):
  categories = Category.query.all()
  category = Category.query.filter_by(id=id).first_or_404()
  if 'search' in request.form:
    search = request.form.get('search')
    books = Book.query.filter(Book.category==category, Book.title.like(f"%{search}%")).all()
    print("here", books)
    return render_template("home.html", current_user=current_user, books=books, categories=categories)
  
  books = category.books
  return render_template("home.html", current_user=current_user, books=books, categories=categories)

@home.route("/<int:id>/book")
@login_required
def book(id):
  book = Book.query.get_or_404(id)
  return render_template("book.html", current_user=current_user, book=book)

@home.route('/book/<int:id>/like')
@login_required
def likebook(id):
  book = Book.query.get_or_404(id)
  current_user.favor.append(book)

  try:
    db.session.commit()
    flash("Book Liked Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('home.book', id=id))

@home.route('/book/<int:id>/unlike')
@login_required
def unlike(id):
  book = Book.query.get_or_404(id)
  current_user.favor.remove(book)
  try:
    db.session.commit()
    flash("Book UnLiked Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('home.profile', id=id))

@home.route('/profile')
@login_required
def profile():
  favorites = current_user.favor
  return render_template("profile.html", current_user=current_user, favorites=favorites)

@home.route("/download/<filename>")
@login_required
def download(filename):
    down_path = "static/uploads/books/" + filename
    print(down_path + filename)
    # return send_from_directory(down_path, filename)
    return send_file(down_path, as_attachment=True)