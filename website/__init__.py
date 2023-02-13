from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = 'website/static/uploads'

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "secretKey"
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  # Add Database
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  from .home import home
  from .auth import auth
  from .admin import admin

  app.register_blueprint(home, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(admin, url_prefix='/admin')

  migrate = Migrate(app, db)

  with app.app_context():
    db.create_all()

  from .models import User
  
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))
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