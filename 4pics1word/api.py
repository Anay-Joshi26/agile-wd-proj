from flask import render_template, jsonify, request, Blueprint, flash, redirect, url_for
from process_game import processGame, isValidGameTitleOrHint, isValidAnswer

api = Blueprint("api", __name__)


@api.route("/api/upload-game", methods=["POST", "GET"])
def uploadGame():
    if request.method == "POST":
        # Handle input validation here, e.g same image inputs,
        # empty inputs, character limits, regex rules etc
        game_title = request.form.get('game-title').strip()
        answer = request.form.get("answer").strip()
        hint = request.form.get("hint").strip()

        if not isValidGameTitleOrHint(game_title):
            return jsonify({"success": False, "game-title-error":True, "msg": "Enter a valid game title"})
        
        if len(hint) != 0 and not isValidGameTitleOrHint(hint):
            return jsonify({"success": False, "hint-error":True, "msg": "Enter a valid hint"})
        
        if not isValidAnswer(answer):
            return jsonify({"success": False, "answer-error":True, "msg": "Answer is invalid"})

        print(f"The game title is |{request.form.get('game-title')}|")



        if len(request.files) != 4:
            flash("Please upload 4 images")
            return jsonify({"success": False, "msg": "Please upload 4 images"})

        filenames = []
        for i in range(1, 5):
            file_key = 'image' + str(i)
            filename = request.files[file_key].filename
            filenames.append(filename)
            if file_key not in request.files or filename == '':
                print(f"Image {i} is missing or empty")
                return jsonify({"success": False, "image-error":True, "msg": f"Image {i} is missing or empty"})
            
        if len(set(filenames)) != len(filenames):
            return jsonify({"success": False, "image-error": True, "msg": "Duplicate images detected"}) 
        
        outcome = processGame(game_title, request.files, answer, hint)

        if not outcome:
            return jsonify({"success": False, "msg": "Failed to upload game"})
        
        return jsonify({"success": True, "msg": "Game uploaded successfully"})









