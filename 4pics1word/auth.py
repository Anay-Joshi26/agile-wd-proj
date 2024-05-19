from flask import redirect, url_for, render_template
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.csrf.session import SessionCSRF
import re



from models import db, User

# generation of unique csrf tokens, and flask_wtf forms for login and register
class CustomCSRF(SessionCSRF):
    def generate_csrf_token(self, csrf_token_field):
        # Generate a unique token based on form's ID or name
        return super().generate_csrf_token(csrf_token_field) + f'-{csrf_token_field.form.id}'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    class Meta:
        csrf = CustomCSRF

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])

    class Meta:
        csrf = CustomCSRF

# check if a user exists
def validate_username(username):
    return User.query.filter_by(username=username).first()

# register a new user by hashing the password
# and adding the user to the database
def register_new_user(username, password, bcrypt):
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username = username, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()


# login a new user by checking if the password
# matches the hashed password in the database
# and logging the user in
def login_new_user(username, password, bcrypt):
    user = validate_username(username) 
    if user:
        if bcrypt.check_password_hash(user.password, password):
            print(user.username)
            login_user(user)
            return True
    return False
    

# check if a username and password is valid
# using server side regex
def isValidUsername(username):
    return re.match(r'^[a-zA-Z0-9_]+$', username)

def isValidPassword(password):
    return re.match(r'^.+$', password)

    
