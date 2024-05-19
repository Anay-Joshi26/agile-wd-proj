import sys
import os

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from flask import Flask
from models import db, User
from blueprints import api, tests, main
from flask_login import LoginManager
#import main

def create_app(config):

    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    flask_app.register_blueprint(api)
    flask_app.register_blueprint(tests)
    flask_app.register_blueprint(main)
    db.init_app(flask_app)

    login_manager = LoginManager()
    login_manager.init_app(flask_app)
    login_manager.login_view = "index"

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return flask_app