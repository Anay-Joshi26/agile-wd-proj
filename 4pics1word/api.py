from flask import render_template, jsonify, request, Blueprint, flash, redirect, url_for
from process_game import processGame, isValidGameTitleOrHint, isValidAnswer, UPLOAD_FOLDER
from flask import send_from_directory
from flask_login import current_user
from models import Game, db

api = Blueprint("api", __name__)

@api.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


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
            return jsonify({"success": False, "image-error": True, "msg": "Duplicate filenames detected, ensure that all filenames are unique"}) 
        
        outcome = processGame(game_title, request.files, answer, hint)

        if not outcome:
            return jsonify({"success": False, "msg": "Failed to upload game"})
        
        return jsonify({"success": True, "msg": "Game uploaded successfully"})
    
@api.route("/api/upvote/<int:game_id>", methods=["POST", "GET"])
def upvote(game_id):
    if not current_user.is_authenticated:
        print("User is not authenticated")
        return jsonify({"success": False, "msg": "You need to be logged in to upvote"})
    
    game = Game.query.filter_by(gameId=game_id).first()
    if game is None:
        return jsonify({"success": False, "msg": "Game not found"})
    
    game.number_of_upvotes += 1
    db.session.commit()
    
    return jsonify({"success": True, "msg": "Upvoted successfully"})

@api.route("/api/downvote/<int:game_id>", methods=["POST", "GET"])
def downvote(game_id):
    if not current_user.is_authenticated:
        print("User is not authenticated")
        return jsonify({"success": False, "msg": "You need to be logged in to upvote"})
    
    game = Game.query.filter_by(gameId=game_id).first()
    if game is None:
        return jsonify({"success": False, "msg": "Game not found"})
    
    game.number_of_upvotes -= 1
    db.session.commit()
    
    return jsonify({"success": True, "msg": "Upvoted successfully"})









