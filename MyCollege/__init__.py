from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import SECRET_KEY, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, DB_CON_STR

login_manager = LoginManager()

def create_app():
  app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
  app.secret_key = SECRET_KEY
  app.config['DB_NAME'] = DB_NAME
  app.config['DB_USER'] = DB_USER
  app.config['DB_PASS'] = DB_PASS
  app.config['DB_HOST'] = DB_HOST
  app.config['DB_PORT'] = DB_PORT
  app.config['DB_CON_STR'] = DB_CON_STR

  CSRFProtect(app)

  # Initialize login manager
  login_manager.init_app(app)
  login_manager.login_view = 'user.login'
  login_manager.login_message = 'Please log in to access this page.'

  from .controllers.general import general_bp as general_blueprint
  from .controllers.college import college_bp as college_blueprint
  from .controllers.program import program_bp as program_blueprint
  from .controllers.student import student_bp as student_blueprint
  from .controllers.user import user_bp as user_blueprint

  app.register_blueprint(general_blueprint)
  app.register_blueprint(college_blueprint)
  app.register_blueprint(program_blueprint)
  app.register_blueprint(student_blueprint)
  app.register_blueprint(user_blueprint)

  # User loader callback for Flask-Login
  @login_manager.user_loader
  def load_user(user_id):
    from MyCollege.models.models import Users
    return Users.get_by_id(user_id)
  
  return app