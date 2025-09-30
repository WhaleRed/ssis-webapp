from flask import Flask
from config import SECRET_KEY

def create_app():
  app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
  app.secret_key = SECRET_KEY

  from .controllers.general import general_bp as general_blueprint
  from .controllers.college import college_bp as college_blueprint
  from .controllers.program import program_bp as program_blueprint
  app.register_blueprint(general_blueprint)
  app.register_blueprint(college_blueprint)
  app.register_blueprint(program_blueprint)
  return app