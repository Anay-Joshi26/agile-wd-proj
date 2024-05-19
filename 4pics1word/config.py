import os
from dotenv import load_dotenv

load_dotenv()

# Config class for the app
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY_APP')
    print(SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))

# test config for unit tests (not with selenium)
class TestConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY_APP')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
    TESTING = True


