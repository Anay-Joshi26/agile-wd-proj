from flask import render_template, jsonify, request, Blueprint, flash, redirect, url_for
from process_game import processGame

api = Blueprint("api", __name__)


@api.route("/api/upload-game", methods=["POST", "GET"])
def uploadGame():
    if request.method == "POST":
        # Handle input validation here, e.g same image inputs,
        # empty inputs, character limits, regex rules etc

        if len(request.files) != 4:
            flash("Please upload 4 images")
            return jsonify({"success": False, "message": "Please upload 4 images"})

        filenames = []
        for i in range(1, 5):
            file_key = 'image' + str(i)
            filename = request.files[file_key].filename
            filenames.append(filename)
            if file_key not in request.files or filename == '':
                print(f"Image {i} is missing or empty")
                return jsonify({"success": False, "message": f"Image {i} is missing or empty"})
            
        if len(set(filenames)) != len(filenames):
            return jsonify({"success": False, "message": "Duplicate images detected"}) 
        
        outcome = processGame(request.form.get("game-title"), request.files, request.form.get("answer"), request.form.get("hint"))

        if not outcome:
            return jsonify({"success": False, "message": "Failed to upload game"})
        
        return jsonify({"success": True, "message": "Game uploaded successfully"})









