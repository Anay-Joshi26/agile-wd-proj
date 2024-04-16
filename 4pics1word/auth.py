from flask import redirect, url_for, render_template
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from models import db, User

def validate_username(username):
    return User.query.filter_by(username=username).first()

def register_new_user(username, password, bcrypt):
    user_check = validate_username(username)
    if user_check:
        return render_template("register.html")
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username = username, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

def login_new_user(username, password, bcrypt):
    user = validate_username(username) 
    if user:
        if bcrypt.check_password_hash(user.password, password):
            print(user.username)
            login_user(user)
    else:
        return redirect(url_for('login'))

    
