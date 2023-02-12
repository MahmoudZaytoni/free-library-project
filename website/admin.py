import os
from flask import Blueprint, render_template, redirect, url_for, request, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import BookForm
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
  if request.method == "GET":
    book = db.session.query(Book).filter(Book.id==id).first()
    form = BookForm()
    down_path = "uploads/books/"
    form.title.data = book.title
    form.author.data = book.author
    form.cover.data = down_path + book.cover
    form.book.data = down_path + book.file_name
    form.desc.data = book.desc
    return render_template("book-form.html", user=current_user, form=form, operation="Change Book")


@admin.route('/book/<int:id>/delete')
def delete():
  pass