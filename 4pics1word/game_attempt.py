from models import db, Attempt, GamePerformance
from flask_login import current_user

# record a user's current attempt at a game
# so that if they re-visit the site their attempt count will persist
# if they get the answer correct, their performance will be recorded (ie added to leaderboard)
def record_attempt(guess, attempt_count, correct, game):
    new_attempt = Attempt(guess = guess, correct = correct, attempts = attempt_count, game = game, player = current_user)
    db.session.add(new_attempt)
    db.session.commit()

    if correct:
        new_game_performance = GamePerformance(game = game, user = current_user, attempts = attempt_count)
        db.session.add(new_game_performance)
        db.session.commit()

    return None