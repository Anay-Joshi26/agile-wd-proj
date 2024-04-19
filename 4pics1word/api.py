from flask import render_template, jsonify, request, Blueprint
from process_game import processGame

api = Blueprint("api", __name__)

@api.route("/api/upload-game", methods=["POST", "GET"])
def uploadGame():
    if request.method == "POST":
        # Handle input validation here, e.g same image inputs,
        # empty inputs, character limits, regex rules etc
        
        processGame(request.form.get("game-title"), request.files['image1'], request.files['image2'], \
                    request.files['image3'], request.files['image4'], request.form.get("answer"), request.form.get("hint"))
        return jsonify({"message": "Game uploaded successfully"})









