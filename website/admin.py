import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import BookForm, BookFormUpdate
from . import db, UPLOAD_FOLDER
from .models import Book

admin = Blueprint('admin', __name__)

@admin.route('/')
def dash():
  return render_template('admin.html', user=current_user)

@admin.route('/book')
def readbooks():
  books = Book.query.order_by(Book.id).all()
  return render_template('books.html', user=current_user, books=books)

@admin.route('/book/add', methods=["GET", "POST"])
def addbook():
  form = BookForm()
  if form.validate_on_submit():
    title = form.title.data
    author = form.author.data
    cover = form.cover.data
    book = form.book.data
    desc = form.desc.data
    cover_filename = secure_filename(cover.filename)
    book_filename = secure_filename(book.filename)
    new_book = Book(title=title, author=author, cover=cover_filename, file_name=book_filename, desc=desc)
    db.session.add(new_book)
    db.session.commit()
    cover.save(os.path.join(UPLOAD_FOLDER + '/covers', cover_filename))
    book.save(os.path.join(UPLOAD_FOLDER + '/books', book_filename))
    return redirect(url_for('admin.readbooks'))
  return render_template('book-form.html', user=current_user, form=form, operation="Add Book")

@admin.route('/book/<int:id>/change', methods=["GET", "POST"])
def changebook(id):
  form = BookFormUpdate()
  book = Book.query.get_or_404(id)
  upload_path = "uploads/"

  if request.method == "GET":
    form.title.data = book.title
    form.author.data = book.author
    form.cover.data = upload_path + "covers/" + book.cover
    form.book.data = upload_path + "books/" + book.file_name
    form.desc.data = book.desc
    return render_template("book-form.html", user=current_user, form=form, operation="Change Book")
  else:
    book.title = form.title.data
    book.author = form.author.data
    book.desc = form.desc.data
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
    
  return redirect(url_for('admin.readbooks'))



@admin.route('/book/<int:id>/delete')
def deletebook(id):
  book_to_delete = Book.query.get_or_404(id)

  try:
    db.session.delete(book_to_delete)
    db.session.commit()
    flash("Book Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('admin.readbooks'))
