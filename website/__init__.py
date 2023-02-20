from flask import Flask
from .extensions import db, login_manager, migrate

UPLOAD_FOLDER = ""

def create_app():
  app = Flask(__name__, instance_relative_config=True)

  app.config.from_object('config')
  app.config.from_pyfile('config.py')


  global UPLOAD_FOLDER 
  UPLOAD_FOLDER= app.config['UPLOAD_FOLDER']
  
  db.init_app(app)

  from .home import home
  from .auth import auth
  from .admin import admin
  from .author.routes import author

  app.register_blueprint(home, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(admin, url_prefix='/admin')
  app.register_blueprint(author, url_prefix='/')


  migrate.init_app(app, db)

  with app.app_context():
    db.create_all()

  from .models import User
  
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app