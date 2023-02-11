from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import LoginForm, SignUpForm

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    flash('Test Form Succesfuly', category='success')
    return redirect(url_for('view.index'))
  
  return render_template('login.html', form=form)

##############################################################

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
  form = SignUpForm()

  if form.validate_on_submit():
    flash('Test Form Succesfuly', category='success')
    return redirect(url_for('view.index'))
  
  return render_template('signup.html', form=form)