from flask import Blueprint, render_template
from flask_login import current_user
views = Blueprint('view', __name__)

@views.route("/")
def index():
  return render_template("home.html", user=current_user)

