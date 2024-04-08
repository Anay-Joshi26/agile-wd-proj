from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create instance of Database
from models import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

PORT = 5000

# Web page routing
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    return render_template("register.html")

@app.route("/challenges")
def challenges_page():
    return render_template("challenge-board.html")

@app.route("/challenge/<int:challenge_id>")
def challenge_page(challenge_id):
    return f"Challenge {challenge_id}"
# hello

if __name__ == '__main__':
    app.run(debug=True, port = PORT)
