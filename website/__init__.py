from flask import Flask, abort
from .extensions import db, login_manager, migrate

UPLOAD_FOLDER = ""
def is_accessable(id):
  # Check if id is an admin id
  if int(id) in set([1, 2, 3]):
    return True
  return abort(404)

def create_app():
  app = Flask(__name__, instance_relative_config=True)

  app.config.from_object('config')
  app.config.from_pyfile('config.py')


  global UPLOAD_FOLDER 
  UPLOAD_FOLDER= app.config['UPLOAD_FOLDER']
  
  db.init_app(app)

  from .home.routes import home
  from .auth.routes import auth
  from .book.routes import book
  from .category.routes import category
  from .author.routes import author
  from .admin import admin

  app.register_blueprint(admin, url_prefix='/admin')
  app.register_blueprint(home, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(book, url_prefix='/')
  app.register_blueprint(author, url_prefix='/')
  app.register_blueprint(category, url_prefix='/')


  migrate.init_app(app, db)

  with app.app_context():
    db.create_all()

  from .models import User
  
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app