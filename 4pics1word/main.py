from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

PORT = 5000

@app.route("/")
def hello_world():
    return render_template("index.html")

# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     return render_template("login.html")

# @app.route("/register", methods=['POST', 'GET'])
# def register():
#     return render_template("register.html")

@app.route("/challenges")
def challenges_page():
    return render_template("challenge-board.html")

@app.route("/challenge/<int:challenge_id>")
def challenge_page(challenge_id):
    return f"Challenge {challenge_id}"
# hello

if __name__ == '__main__':
    app.run(debug=True, port = PORT)
    