from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.String, nullable = False)
    clue1 = db.Column(db.String, nullable = False)
    clue2 = db.Column(db.String, nullable = False)
    clue3 = db.Column(db.String, nullable = False)
    image1 = db.Column(db.LargeBinary, nullable = False)
    image2 = db.Column(db.LargeBinary, nullable = False)
    image3 = db.Column(db.LargeBinary, nullable = False)
    image4 = db.Column(db.LargeBinary, nullable = False)