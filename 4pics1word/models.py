from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key = True)
    game_title = db.Column(db.String, nullable = False)
    answer = db.Column(db.String, nullable = False)
    hint = db.Column(db.String, nullable = True)
    image1 = db.Column(db.String, nullable = False)
    image2 = db.Column(db.String, nullable = False)
    image3 = db.Column(db.String, nullable = False)
    image4 = db.Column(db.String, nullable = False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # the backref tag allows to access all the games created by a user
    # it may be useful for future features such as for a user profile
    creator = db.relationship('User', backref='created_games') 
    number_of_upvotes = db.Column(db.Integer, nullable = False, default=0) # default value is 0 for when it is first created
    # the time will automatically be set to the current time when a game is created
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.now)


class Attempt(db.Model):
    attempt_id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game = db.relationship('Game', backref='played_games')
    player = db.relationship('User', backref='player')
    

class GamePerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # the person who played the game
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # the game that was played
    game = db.relationship('Game', backref='game_performances')
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable=False)
    attempts = db.Column(db.Integer, nullable=False)

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User')
    game = db.relationship('Game')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable=False)
    vote = db.Column(db.Integer, nullable=False, default=0)

    # reference https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
    # this should essentilly ensure that a user can only upvote a game once
    __table_args__ = (db.UniqueConstraint('user_id', 'game_id'),)

