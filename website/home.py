from flask import Blueprint, render_template
from flask_login import current_user, login_required

home = Blueprint('home', __name__)

@home.route("/")
@login_required
def index():
  return render_template("home.html", user=current_user)

  

