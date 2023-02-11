from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "secretKey"

  # Add Database
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')

  with app.app_context():
    db.create_all()
  # Create Custom Error Pages

  # - Invalid Url 
  @app.errorhandler(404)
  def page_not_found(e):
    type_error = "404 Error"
    message = "Page Not Found - Try Again.."
    return render_template("base-error.html", type_error=type_error, message=message), 404

  # - Internal Server Error
  @app.errorhandler(500)
  def server_error(e):
    type_error = "505 Internal Server Error"
    message = "Try Again.."
    return render_template("500.html"), 500
  
  return app