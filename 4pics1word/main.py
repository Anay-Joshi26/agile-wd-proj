
from flask import Flask, url_for, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt
from auth import register_new_user, login_new_user, validate_username, isValidUsername, isValidPassword
from api import api
from process_game import UPLOAD_FOLDER
from game_attempt import record_attempt


# Create instance of Database
from models import db, User, Game, Attempt
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

app.register_blueprint(api)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(app.config['UPLOAD_FOLDER'])

PORT = 5000

# Logging in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Web page routing
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/challenges/create-game", methods=['POST', 'GET'])
@login_required
def create_game():
    return render_template("create_game.html")

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
@login_required
def challenges_page():
    return render_template("challenge-board.html")

@app.route("/challenge/<int:challenge_id>")
@login_required
def challenge_page(challenge_id):
    game = Game.query.filter_by(gameId = challenge_id).first()

    if game == None:
        return redirect(url_for('challenges_page'))
    
    message = ""

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

    return render_template("challenge.html", hint = game.hint, attempt_count = (attempt_count + 1), answer = game.answer, image1 = game.image1, image2 = game.image2, image3 = game.image3, image4 = game.image4, challenge_id = challenge_id, message = message)
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
    app.run(debug=True, port = PORT)
