from flask import Flask
from flask_migrate import Migrate
from .extensions import db, login_manager, migrate

def create_app(config_file='settings.py'):
  app = Flask(__name__)

  app.config.from_pyfile(config_file)

  db.init_app(app)

  from .home import home
  from .auth import auth
  from .admin import admin

  app.register_blueprint(home, url_prefix ='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(admin, url_prefix='/admin')

  migrate.init_app(app, db)

  with app.app_context():
    db.create_all()

  from .models import User
  
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app