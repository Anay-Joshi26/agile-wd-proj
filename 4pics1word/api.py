from flask import render_template, jsonify, request, Blueprint, flash, redirect, url_for
from process_game import processGame, isValidGameTitleOrHint, isValidAnswer, UPLOAD_FOLDER
from flask import send_from_directory
from flask_login import current_user
import math
from models import Game, db, User, Upvote

from blueprints import api

# enable the api to serve static files
# to reach/render the game images
@api.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# endpoint to upload a game
@api.route("/api/upload-game", methods=["POST", "GET"])
def uploadGame():
    if request.method == "POST":
        # Handle input validation here, e.g same image inputs,
        # empty inputs, character limits, regex rules etc
        game_title = request.form.get('game-title').strip()
        answer = request.form.get("answer").strip()
        hint = request.form.get("hint").strip()

        # Validate the inputs, for title, hint, answer etc
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

        # do validation checks on the images
        # such as duplicate images
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
        
        # Process the game
        outcome = processGame(game_title, request.files, answer, hint)

        if not outcome:
            return jsonify({"success": False, "msg": "Failed to upload game"})
        
        return jsonify({"success": True, "msg": "Game uploaded successfully"})
    

# endpoint to upvote a game
@api.route("/api/upvote/<int:game_id>", methods=["POST", "GET"])
def upvote(game_id):

    if not current_user.is_authenticated:
        #print("User is not authenticated")
        return jsonify({"success": False, "msg": "You need to be logged in to upvote"})
    
    game = Game.query.filter_by(gameId=game_id).first()
    if game is None:
        return jsonify({"success": False, "msg": "Game not found"})

    existing_vote = Upvote.query.filter_by(user=current_user, game=game).first()
    if existing_vote is not None:
        if existing_vote.vote == 1:  # If already upvoted
            return jsonify({"success": False, "msg": "You have already upvoted this game"})
        else:  # If downvoted
            existing_vote.vote += 1
            game.number_of_upvotes += 1 
    else:
        downvote = Upvote(user=current_user, game=game, vote=1)
        game.number_of_upvotes += 1
        db.session.add(downvote)

    db.session.commit()
    
    return jsonify({"success": True, "msg": "Upvoted successfully"})


# endpoint to downvote a game
@api.route("/api/downvote/<int:game_id>", methods=["POST", "GET"])
def downvote(game_id):
    if not current_user.is_authenticated:
        print("User is not authenticated")
        return jsonify({"success": False, "msg": "You need to be logged in to downvote"})
    
    game = Game.query.filter_by(gameId=game_id).first()
    if game is None:
        return jsonify({"success": False, "msg": "Game not found"})
    
    existing_vote = Upvote.query.filter_by(user=current_user, game=game).first()
    if existing_vote is not None:
        if existing_vote.vote == -1:  # If already downvoted
            return jsonify({"success": False, "msg": "You have already downvoted this game"})
        else:  # If upvoted
            existing_vote.vote -= 1
            game.number_of_upvotes -= 1 
    else:
        downvote = Upvote(user=current_user, game=game, vote=-1)
        game.number_of_upvotes -= 1
        db.session.add(downvote)

    db.session.commit()
    
    return jsonify({"success": True, "msg": "downvoted successfully"})

# endpoint to get all the games in a paginated manner
# so the client side js can load/request more games based on api calls
@api.route('/api/games', methods=["POST", "GET"])
def get_games():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)
        

    games = Game.query.paginate(page=page, per_page=limit)

    # Get the user's votes, whether they have upvoted or downvoted a game (or nothihg)
    user_votes = {}
    if current_user.is_authenticated:
        user_votes_query = db.session.query(Upvote.game_id, Upvote.vote).filter_by(user_id=current_user.id).all()
        user_votes = {game_id: vote for game_id, vote in user_votes_query}

    serialised_games = [ 
        {
            'gameId': game.gameId,
            'game_title': game.game_title,
            'creator_username': game.creator.username,
            'number_of_upvotes': game.number_of_upvotes,
            'image1': game.image1,
            'image2': game.image2,
            'image3': game.image3,
            'image4': game.image4,
            'date_created': game.date_created,
            'user_vote': user_votes.get(game.gameId, 0)  # If no vote found, default to 0
        }
        for game in games.items
    ]

    return jsonify({"success": True, "games": serialised_games})









