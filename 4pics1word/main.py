from flask import Flask, url_for, render_template, request, redirect, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt
from io import BytesIO
import base64

from auth import register_new_user, login_new_user, validate_username, isValidUsername, isValidPassword

# Create instance of Database
from models import db, User, Game
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

PORT = 5000

# Logging in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# def encode_image(image_path):
#     with open(image_path, 'rb') as f:
#         image_binary = f.read()
#         encoded_image = base64.b64encode(image_binary)
#     return encoded_image

# Web page routing
@app.route("/")
def index():
    # encode = encode_image("duck.png")
    # game = Game(answer = "duck", clue1 = "goose", clue2 = "circle", clue3 = "chase", image1 = encode, image2 = encode, image3 = encode, image4 = encode)
    # db.session.add(game)
    # db.session.commit()
    return render_template("index.html")

@app.route("/challenges/create-game", methods=['POST', 'GET'])
def create_game():
    return render_template("create_game.html")


# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     return render_template("login.html")
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username').strip()
#         password = request.form.get('password')
#         is_valid_username = isValidUsername(username)
#         if not is_valid_username:
#             jsonify({'username-error': True})
#         is_valid_password = isValidPassword(username)
#         if not is_valid_password:
#             jsonify({'password-error': True})
#         user_check = validate_username(username) 
#         if user_check:
#             login_new_user(username,password, bcrypt)
#             return redirect(url_for('dashboard'))
    
#     return redirect(url_for('index'))

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        print(username, password)

        is_valid_username = isValidUsername(username)
        if not is_valid_username:
            return jsonify({'success': False, 'regex-error':'username', 'msg': 'Invalid Username'})  
        
        print("checkk")
        is_valid_password = isValidPassword(username)
        if not is_valid_password:
            return jsonify({'success': False, 'regex-error':'password', 'msg':'Invalid Password'})  
        
        user_check = validate_username(username) 

        print(user_check)

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

        print(user_check, "heyoo")


        
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
    return render_template("challenge-board.html")

@app.route("/challenge/<int:challenge_id>")
@login_required
def challenge_page(challenge_id):
    return render_template("challenge.html", answer = 'THIS IS AWESOME')

@app.route("/get_image/<int:challenge_id>/<int:image_id>")
@login_required
def get_image(challenge_id, image_id):
    game = Game.query.filter_by(gameId=challenge_id).first()

    if image_id == 1:
        image = BytesIO(base64.b64decode(game.image1))
    elif image_id == 2:
        image = BytesIO(base64.b64decode(game.image2))
    elif image_id == 3:
        image = BytesIO(base64.b64decode(game.image3))
    elif image_id == 4:
        image = BytesIO(base64.b64decode(game.image4))

    return send_file(image, mimetype='image/jpeg')

@app.route("/<int:challenge_id>/answer")
@login_required
def api():
    data = {'message': 'THIS IS AWESOME'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port = PORT)
