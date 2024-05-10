import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


from flask import Flask, url_for, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt
from auth import register_new_user, login_new_user, validate_username, isValidUsername, isValidPassword
from api import api
from process_game import UPLOAD_FOLDER
from generate_fake_data import generate_all_games
from flask_migrate import Migrate
from datetime import datetime, timedelta


# Create instance of Database
from models import db, User, Game
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

migrate = Migrate(app, db)

# db.init_app(app)

# with app.app_context():
#     db.create_all()

bcrypt = Bcrypt(app)

app.register_blueprint(api)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(app.config['UPLOAD_FOLDER'])

PORT = 5000

FAKE_DATA = True

db.init_app(app)

with app.app_context():
    db.create_all()
    if FAKE_DATA and not User.query.first():
        generate_all_games()

    
# Logging in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Web page routing
@app.route("/")
def index():
    login_modal = request.args.get('login')
    return render_template("index.html", login_modal = login_modal, is_index = True)


@app.route("/challenges/create-game", methods=['POST', 'GET'])
@login_required
def create_game():
    return render_template("create_game.html")

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You need to be logged in to access this page.')
    return redirect('/?login=true')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

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
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        is_valid_username = isValidUsername(username)
        if not is_valid_username:
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
    return render_template("challenge-board.html", current_user=current_user, games=games, trending_games=trending_games)

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
    return f"Challenge {challenge_id}"
# hello

if __name__ == '__main__':
    app.run(debug=True, port = PORT)
