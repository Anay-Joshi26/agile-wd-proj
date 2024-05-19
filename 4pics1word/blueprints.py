from flask import Blueprint

# define blueprints for the different parts of the application

# api allows for the creation of games and upvoting
api = Blueprint("api", __name__)

tests = Blueprint("testing", __name__)

main = Blueprint("main", __name__)

