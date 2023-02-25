from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .extensions import db
from .models import User
from . import is_accessable

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def dash():
  is_accessable(current_user.id)
  return render_template('admin.html', current_user=current_user)

#################################### Users ###########################################
@admin.route('/users')
@login_required
def readusers():
  is_accessable(current_user.id)
  users = User.query.order_by(User.id).all()
  return render_template('users.html', current_user=current_user, users=users)

@admin.route('/user/<int:id>/delete')
@login_required
def delete_user(id):
  is_accessable(current_user.id)
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