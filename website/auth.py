from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .forms import LoginForm, SignUpForm
from .models import User

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
      flash(f"Welcome Back {user.first_name}!\n Start having Fun with our free books",category='success')
      login_user(user, remember=True)
      return redirect(url_for("home.index"))
    else:
      flash("Incorrect Email or Password ", category='error')
  return render_template('login.html', form=form, current_user=current_user)

##############################################################

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

##############################################################

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
  form = SignUpForm()

  if form.validate_on_submit():
    first_name = form.first_name.data
    email = form.email.data
    password1 = form.password1.data
    password2 = form.password2.data
    user = User.query.filter_by(email=email).first()
    if user:
      flash("Email Already Exist. ", category='error')
    elif password1 != password2:
      flash("Password don't match ", category='error')
    else:
      new_user = User(first_name=first_name, email=email, password=generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash(f"Welcome {first_name}\nStart having fun with our Free books", category='success')
      return redirect(url_for("home.index")) 
  return render_template('signup.html', form=form, current_user=current_user)