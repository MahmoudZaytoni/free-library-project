from flask import Blueprint, render_template, redirect, flash, url_for, send_file, request
from flask_login import current_user, login_required
from .models import Book
from . import db
home = Blueprint('home', __name__)

@home.route("/", methods=["GET", "POST"])
@login_required
def index():
  if 'search' in request.form:
    print("here")
    search = request.form.get('search')
    books = Book.query.filter(Book.title.like(f"%{search}%")).all()
  else:
    books = Book.query.all()
  return render_template("home.html", user=current_user, books=books)

@home.route("/<int:id>/book")
def book(id):
  book = Book.query.get_or_404(id)
  return render_template("book.html", user=current_user, book=book)


@home.route('/book/<int:id>/like')
def likebook(id):
  book = Book.query.get_or_404(id)
  current_user.favor.append(book)

  try:
    db.session.commit()
    flash("Book Liked Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('home.book', id=id))


@home.route('/profile')
def profile():
  favorites = current_user.favor
  return render_template("profile.html", user=current_user, favorites=favorites)

@home.route("/download/<filename>")
def download(filename):
    down_path = "static/uploads/books/" + filename
    print(down_path + filename)
    # return send_from_directory(down_path, filename)
    return send_file(down_path, as_attachment=True)