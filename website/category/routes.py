from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .forms import CategoryForm
from ..extensions import db
from ..models import Category
from .. import is_accessable

category = Blueprint('category', __name__, template_folder='templates', static_folder='static')

@category.route('/categories')
@login_required
def read_categories():
  is_accessable(current_user.id)
  categories = Category.query.order_by(Category.id).all()
  return render_template('categories.html', current_user=current_user, categories=categories)

@category.route('/category/add', methods= ["GET", "POST"])
@login_required
def add_category():
  is_accessable(current_user.id)
  form = CategoryForm()
  if form.validate_on_submit():
    category_name = form.category.data 
    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('category.read_categories'))
  return render_template('category-form.html', current_user=current_user, form=form, operation="Add Category")

@category.route('/category/<int:id>/change', methods=["GET", "POST"])
@login_required
def change_category(id):
  is_accessable(current_user.id)
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
  return redirect(url_for('category.read_categories'))

@category.route('/category/<int:id>/delete')
@login_required
def delete_category(id):
  is_accessable(current_user.id)
  category_to_delete = Category.query.get_or_404(id)

  try:
    db.session.delete(category_to_delete)
    db.session.commit()
    flash("Category Deleted Successfuly")
  except:
    flash("Error", message='error')
  return redirect(url_for('category.read_categories'))