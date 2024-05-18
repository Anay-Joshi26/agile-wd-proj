import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


from flask import Flask, url_for, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt
from auth import register_new_user, login_new_user, validate_username, isValidUsername, isValidPassword, LoginForm, RegisterForm, CustomCSRF
from api import api
from process_game import UPLOAD_FOLDER
from game_attempt import record_attempt
from generate_fake_data import generate_all_games
from flask_migrate import Migrate
from config import Config
from blueprints import main
from datetime import datetime, timedelta


# Create instance of Database
from models import db, User, Game, Attempt, GamePerformance
from __init__ import create_app

app = create_app(Config)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

PORT = 5000

FAKE_DATA = True

with app.app_context():
    db.create_all()
    if FAKE_DATA and not User.query.first():
        generate_all_games()

    
# Logging in
login_manager = app.login_manager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "index"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# Web page routing
@app.route("/")
def index():
    login_modal = request.args.get('login')
    loginform = LoginForm()
    registerform = RegisterForm()
    return render_template("index.html", login_modal = login_modal, is_index = True, loginform = loginform, registerform = registerform, login_token = CustomCSRF, register_token = CustomCSRF)


@app.route("/challenges/create-game", methods=['POST', 'GET'])
@login_required
def create_game():
    loginform = LoginForm()
    registerform = RegisterForm()
    return render_template("create_game.html", loginform = loginform, registerform = registerform)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You need to be logged in to access this page.')
    return redirect('/?login=true')

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        is_valid_username = isValidUsername(username)
        if not is_valid_username:
            return jsonify({'success': False, 'regex-error':'username', 'msg': 'Invalid Username'})  
        
        is_valid_password = isValidPassword(username)
        if not is_valid_password:
            return jsonify({'success': False, 'regex-error':'password', 'msg':'Invalid Password'})  
        
        user_check = validate_username(username) 


        if not user_check:
            return jsonify({'success': False, 'user-exists': False, 'msg': 'Username does not exist'})
        
        password_matches_username = login_new_user(username, password, bcrypt)

        if password_matches_username:
            return jsonify({'success': True})  
        
        return jsonify({'success': False, 'incorrect-password': True ,'msg': 'Incorrect password for username'})


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        confirmPassword = form.confirm_password.data
        
        print(username, password, confirmPassword)

        is_valid_username = isValidUsername(username)
        if not is_valid_username:
            print(username, password, confirmPassword)
            return jsonify({'success': False, 'regex-error':'username', 'msg': 'Invalid Username'})  
        
        is_valid_password = isValidPassword(username)
        if not is_valid_password:
            return jsonify({'success': False, 'regex-error':'password', 'msg':'Invalid Password'})  

        if password != confirmPassword:
            return jsonify({'success': False, 'non-matching-passwords': True, 'msg': 'Passwords do not match'})
        
        user_check = validate_username(username)

        
        if user_check is None:
            register_new_user(username, password, bcrypt)
            return jsonify({'success': True}) 
        else:
            return jsonify({'success': False, 'user-exists': True, 'msg': 'That username already exists'})

    return redirect(url_for('index'))

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/challenges")
def challenges_page():
    games = Game.query.all()
    recent_date = datetime.now() - timedelta(days=7)
    trending_games = Game.query.filter(Game.date_created >= recent_date).order_by(Game.number_of_upvotes.desc()).limit(4).all()
    loginform = LoginForm()
    registerform = RegisterForm()
    print(trending_games[0].game_title)
    return render_template("challenge-board.html", current_user=current_user, games=games, loginform = loginform, registerform = registerform, login_token = CustomCSRF, register_token = CustomCSRF,trending_games=trending_games)


def search_database(query):
    return Game.query.filter(Game.game_title.ilike(f'%{query}%')).all()

@app.route('/api/search_suggestions')
def search_suggestions():
    query = request.args.get('q', '').strip()
    if query:
        results = search_database(query)
        return jsonify([{'title': game.game_title, 'id': game.gameId} for game in results])
    return jsonify([])

@app.route("/challenge/<int:challenge_id>")
def challenge_page(challenge_id):
    loginform = LoginForm()
    registerform = RegisterForm()
    game = Game.query.filter_by(gameId = challenge_id).first()
    leaderboard = GamePerformance.query.filter_by(game_id = challenge_id).order_by(GamePerformance.attempts).limit(10).all()
    return render_template("detailed-challenge.html", game=game, leaderboard=leaderboard, loginform = loginform, registerform = registerform)

@app.route("/challenge/play/<int:challenge_id>")
@login_required
def challenge_play(challenge_id):
    loginform = LoginForm()
    registerform = RegisterForm()
    game = Game.query.filter_by(gameId = challenge_id).first()
    if game == None:
        print("WHATTTTTT")
        return redirect(url_for('challenges_page'))
    
    message = ""
    attempt_count = 0

    if current_user.is_authenticated:
        if current_user.id == game.creator_id:
            message = "This is your game. You can play however your guesses will not be recorded."

        recent_attempt = Attempt.query.filter_by(game_id = challenge_id, player_id = current_user.id).order_by(Attempt.attempt_id.desc()).first()
        attempt_count = 0

        if recent_attempt:
            attempt_count = recent_attempt.attempts
            if recent_attempt.correct:
                if message == "":
                    message = "You have already played this game. You can play again however your guesses will not be recorded."  
                attempt_count = 0
    

    return render_template("challenge.html", hint = game.hint, attempt_count = (attempt_count + 1), answer = game.answer, image1 = game.image1, image2 = game.image2, image3 = game.image3, image4 = game.image4, challenge_id = challenge_id, message = message, loginform = loginform, registerform = registerform, login_token = CustomCSRF, register_token = CustomCSRF)
# hello

@app.route("/guess", methods=["GET", "POST"])
@login_required
def make_guess():
    data = request.json
    game = Game.query.filter_by(gameId = data.get('challenge_id')).first()
    print(game.creator.username, game.creator.id)  
    record_attempt(data.get('guess'), data.get('attempts'), data.get('correct'), game)

    if data.get('correct'):
        print(data)
    return jsonify("WOOOO")

if __name__ == '__main__':
    print("RUNNING APP...")
    app.run(debug=True, port = PORT)
