from models import db, User, Game, Attempt
from flask_login import current_user

def record_attempt(guess, attempt_count, correct, game):
    new_attempt = Attempt(guess = guess, correct = correct, attempts = attempt_count, game = game, player = current_user)
    db.session.add(new_attempt)
    db.session.commit()
    return None