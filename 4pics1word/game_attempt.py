from models import db, Attempt, GamePerformance
from flask_login import current_user

def record_attempt(guess, attempt_count, correct, game):
    new_attempt = Attempt(guess = guess, correct = correct, attempts = attempt_count, game = game, player = current_user)
    db.session.add(new_attempt)
    db.session.commit()

    if correct:
        new_game_performance = GamePerformance(game = game, user = current_user, attempts = attempt_count)
        db.session.add(new_game_performance)
        db.session.commit()

    return None