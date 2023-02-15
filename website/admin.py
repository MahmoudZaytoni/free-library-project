import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import BookForm, BookFormUpdate, CategoryForm
from . import db, UPLOAD_FOLDER
from .models import Book, User, Category

admin = Blueprint('admin', __name__)

@admin.route('/')
def dash():
  return render_template('admin.html', current_user=current_user)

#################################### BOOKS ###########################################
@admin.route('/book')
def readbooks():
  books = Book.query.order_by(Book.id).all()
  return render_template('books.html', current_user=current_user, books=books)

@admin.route('/book/add', methods=["GET", "POST"])
def addbook():
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
    return redirect(url_for('admin.readbooks'))
  return render_template('book-form.html', current_user=current_user, form=form, operation="Add Book")

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
    return render_template("book-form.html", current_user=current_user, form=form, operation="Change Book")
  elif form.validate_on_submit():
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
    
  else:
    return render_template("book-form.html", current_user=current_user, form=form, operation="Change Book")
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

#################################### Users ###########################################
@admin.route('/users')
def readusers():
  users = User.query.order_by(User.id).all()
  return render_template('users.html', current_user=current_user, users=users)

@admin.route('/user/<int:id>/delete')
def delete_user(id):
  user_to_delete = User.query.get_or_404(id)
  if current_user == user_to_delete:
    flash("Cannot Delete Current User")
    return redirect(url_for('admin.readusers'))
  try:
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('admin.readusers'))

#################################### Categories ###########################################
@admin.route('/categories')
def read_categories():
  categories = Category.query.order_by(Category.id).all()
  return render_template('categories.html', current_user=current_user, categories=categories)

@admin.route('/category/add', methods= ["GET", "POST"])
def add_category():
  form = CategoryForm()
  if form.validate_on_submit():
    category_name = form.category.data 
    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('admin.read_categories'))
  return render_template('category-form.html', current_user=current_user, form=form, operation="Add Category")

@admin.route('/category/<int:id>/change', methods=["GET", "POST"])
def change_category(id):
  form = CategoryForm()
  category = Category.query.get_or_404(id)
  if request.method == "GET":
    form.category.data = category.category_name
    return render_template("category-form.html", current_user=current_user, form=form, operation="Change Category")
  elif form.validate_on_submit():
    category.category_name = form.category.data
    try:
      db.session.commit()
      flash('Category Changed Successfuly')
    except:
      flash('Error',category='error')
  else:
    return render_template("category-form.html", current_user=current_user, form=form, operation="Change Category")
  return redirect(url_for('admin.read_categories'))

@admin.route('/category/<int:id>/delete')
def delete_category(id):
  category_to_delete = Category.query.get_or_404(id)

  try:
    db.session.delete(category_to_delete)
    db.session.commit()
    flash("Category Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('admin.read_categories'))