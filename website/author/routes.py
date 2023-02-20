import os
from flask import redirect, render_template, url_for, Blueprint
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .forms import AuthorForm
from ..models import Author
from ..extensions import db
from .. import UPLOAD_FOLDER

author = Blueprint('author', __name__, template_folder='templates', static_folder='static')

@author.route('/admin/author', methods=["GET", "POST"])
def read_authors():
  authors = Author.query.order_by(Author.id).all()
  return render_template('authors.html', authors=authors)

@author.route('/admin/author/add', methods=["GET", "POST"])
def add_author():
  form = AuthorForm()
  if form.validate_on_submit():
    name = form.name.data
    photo = form.photo.data
    desc = form.desc.data
    photo_filename = secure_filename(photo.filename)
    new_author = Author(name=name, photo=photo_filename, desc=desc)
    db.session.add(new_author)
    db.session.commit()
    photo.save(os.path.join(UPLOAD_FOLDER + '/photos', photo_filename))
    return redirect(url_for('author.read_authors'))
  return render_template('author-form.html', current_user=current_user, form=form, operation="Add Author")

@author.route('/admin/author/<int:id>/change')
def change_author(id):
  pass

@author.route('/admin/author/<int:id>/delete')
def delete_author(id):
  pass