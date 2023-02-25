import os
from flask import redirect, render_template, url_for, Blueprint, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .forms import AuthorForm
from ..models import Author
from ..extensions import db
from .. import UPLOAD_FOLDER, is_accessable

author = Blueprint('author', __name__, template_folder='templates', static_folder='static')

@author.route('/admin/author', methods=["GET", "POST"])
@login_required
def read_authors():
  authors = Author.query.order_by(Author.id).all()
  return render_template('authors.html', authors=authors)

@author.route('/admin/author/add', methods=["GET", "POST"])
@login_required
def add_author():
  form = AuthorForm()
  if form.validate_on_submit():
    name = form.name.data
    photo = form.photo.data
    desc = form.desc.data
    photo_filename = secure_filename(photo.filename)
    if (photo_filename != ""):
      new_author = Author(name=name, photo=photo_filename, desc=desc)
      photo.save(os.path.join(UPLOAD_FOLDER + '/photos', photo_filename))
    else:
      new_author = Author(name=name, desc=desc)
    db.session.add(new_author)
    db.session.commit()
    return redirect(url_for('author.read_authors'))
  return render_template('author-form.html', current_user=current_user, form=form, operation="Add Author")

@author.route('/admin/author/<int:id>/change', methods=["GET", "POST"])
@login_required
def change(id):
  author = Author.query.get_or_404(id)
  form = AuthorForm()
  upload_path = 'uploads/photos/'
  if request.method == "GET":
    form.name.data = author.name
    if author.photo:
      form.photo.data = upload_path + author.photo 
    form.desc.data = author.desc
    return render_template("author-form.html", current_user=current_user, form=form, operation="Change Author")
  elif form.validate_on_submit():
    author.name = form.name.data
    author.desc = form.desc.data
    photo_filename = secure_filename(form.photo.data.filename)

    if photo_filename:
      author.photo = photo_filename
      form.photo.data.save(os.path.join(UPLOAD_FOLDER + '/photos', photo_filename))
    
    try:
      db.session.commit()
      flash('Author Changed Successfuly')
    except:
      flash('Error',category='error')
    
  else:
    return render_template("author-form.html", current_user=current_user, form=form, operation="Change author")
  return redirect(url_for('author.read_authors'))

@author.route('/admin/author/<int:id>/delete')
@login_required
def delete(id):
  is_accessable(current_user.id)
  author_to_delete = Author.query.get_or_404(id)

  try:
    db.session.delete(author_to_delete)
    db.session.commit()
    flash("Author Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('author.read_authors'))