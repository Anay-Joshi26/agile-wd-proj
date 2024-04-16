from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt

from auth import register_new_user, login_new_user, validate_username

# Create instance of Database
from models import db, User
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

# Web page routing
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        user_check = validate_username(username) 
        if user_check:
            login_new_user(username,password, bcrypt)
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('index'))

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        user_check = validate_username(username)
        if password != confirmPassword:
            return redirect(url_for('index'))
        elif user_check is None:
            register_new_user(username, password, bcrypt)
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/challenges")
def challenges_page():
    return render_template("challenge-board.html")

@app.route("/challenge/<int:challenge_id>")
def challenge_page(challenge_id):
    return f"Challenge {challenge_id}"
# hello

if __name__ == '__main__':
    app.run(debug=True, port = PORT)
