from flask import Flask

def create_app():
  app = Flask(__name__, template_folder="views/templates", static_folder="views/static")

  from .controllers import general_bp as general_blueprint
  app.register_blueprint(general_blueprint)
  return app