from flask import Blueprint, render_template, redirect, flash, url_for, send_file, request, jsonify
from flask_login import current_user, login_required
from ..models import Book, Category
from ..extensions import db

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

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
  is_in_favorites = False
  favorites = current_user.favor
  for favorite in favorites:
    if favorite.id == id:
      is_in_favorites = True
      break
  return render_template("book.html", current_user=current_user, book=book, is_favor = is_in_favorites)

@home.route('/book/<int:id>/like', methods=["POST"])
@login_required
def likebook(id):
  book = Book.query.get_or_404(id)
  current_user.favor.append(book)
  
  try:
    db.session.commit()
  except:
    flash("Error on database", message='error')
    return redirect(url_for('home.book', id=id))
  
  return jsonify({"likes": len(book.favorites)})

@home.route('/book/<int:id>/unlike', methods=["POST"])
@login_required
def unlike(id):
  book = Book.query.get_or_404(id)
  current_user.favor.remove(book)
  
  try:
    db.session.commit()
  except:
    flash("Error on database", message='error')
    return redirect(url_for('home.book', id=id))
  
  return jsonify({"likes": len(book.favorites)})

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