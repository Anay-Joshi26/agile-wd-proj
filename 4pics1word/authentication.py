from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from models import db, User
# class RegisterForm(FlaskForm):
#     username = StringField(validators=[InputRequired()])

#     password = PasswordField(validators=[InputRequired()])

#     submit = SubmitField("Register")

def validate_username(username):
    existing_username = User.query.filter_by(username=username).first()
    return existing_username
def register_new_user(username, password):
    if validate_username(username):
        raise ValidationError("That username already exists. Please choose a different one.")
    new_user = User(username = username, password = password)
    db.session.add(new_user)
    db.session.commit()
