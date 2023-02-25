import os
from flask import redirect, render_template, url_for, Blueprint, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .forms import BookForm, BookFormUpdate
from ..category.forms import FilterByCategory
from ..models import Book
from ..extensions import db
from .. import UPLOAD_FOLDER, is_accessable

book = Blueprint('book', __name__, template_folder='templates', static_folder='static')

@book.route('/book', methods= ["GET", "POST"])
@login_required
def readbooks():
  is_accessable(current_user.id)
  form = FilterByCategory()
  if request.method == "GET":
    books = Book.query.order_by(Book.id).all()
  if request.method == "POST" and form.validate_on_submit():
    if form.category.data != None:
      books = Book.query.filter_by(category=form.category.data)
    else:
      books = Book.query.order_by(Book.id).all()
  return render_template('books.html', current_user=current_user, books=books, form=form)

@book.route('/book/add', methods=["GET", "POST"])
@login_required
def addbook():
  is_accessable(current_user.id)
  form = BookForm()
  if form.validate_on_submit():
    title = form.title.data
    author = form.author.data
    cover = form.cover.data
    book = form.book.data
    desc = form.desc.data
    category = form.category.data
    cover_filename = secure_filename(cover.filename)
    book_filename = secure_filename(book.filename)
    new_book = Book(title=title, author=author,cover=cover_filename, file_name=book_filename, desc=desc, category=category)
    db.session.add(new_book)
    db.session.commit()
    cover.save(os.path.join(UPLOAD_FOLDER + '/covers', cover_filename))
    book.save(os.path.join(UPLOAD_FOLDER + '/books', book_filename))
    return redirect(url_for('book.readbooks'))
  return render_template('book-form.html', current_user=current_user, form=form, operation="Add Book")

@book.route('/book/<int:id>/change', methods=["GET", "POST"])
@login_required
def changebook(id):
  is_accessable(current_user.id)
  form = BookFormUpdate()
  book = Book.query.get_or_404(id)
  upload_path = "uploads/"

  if request.method == "GET":
    form.title.data = book.title
    form.author.data = book.author
    form.cover.data = upload_path + "covers/" + book.cover
    form.book.data = upload_path + "books/" + book.file_name
    form.desc.data = book.desc
    form.category.data = book.category
    return render_template("book-form.html", current_user=current_user, form=form, operation="Change Book")
  elif form.validate_on_submit():
    book.title = form.title.data
    book.author = form.author.data
    book.desc = form.desc.data
    book.category = form.category.data
    cover_filename = secure_filename(form.cover.data.filename)
    book_filename = secure_filename(form.book.data.filename)

    if cover_filename != "":
      book.cover = cover_filename
      form.cover.data.save(os.path.join(UPLOAD_FOLDER + '/covers', cover_filename))
    
    if book_filename != "":      
      book.file_name = book_filename
      form.book.data.save(os.path.join(UPLOAD_FOLDER + '/books', book_filename))
    
    try:
      db.session.commit()
      flash('Book Changed Successfuly')
    except:
      flash('Error',category='error')
    
  else:
    return render_template("book-form.html", current_user=current_user, form=form, operation="Change Book")
  return redirect(url_for('book.readbooks'))

@book.route('/book/<int:id>/delete')
@login_required
def deletebook(id):
  is_accessable(current_user.id)
  book_to_delete = Book.query.get_or_404(id)

  try:
    db.session.delete(book_to_delete)
    db.session.commit()
    flash("Book Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('book.readbooks'))
