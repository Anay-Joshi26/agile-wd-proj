from werkzeug.utils import secure_filename
import os
from models import db, User, Game
from flask_login import current_user
import re

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Validity checks
def isValidGameTitleOrHint(game_title):
    return len(game_title) <= 75 and len(game_title) > 0

def isValidAnswer(answer):
    return re.match(r"^(?!.*\s\s)(?!^\s)[a-zA-Z0-9\s]{1,24}$", answer)

def buildPath(game_id, filename):
    return f"/uploads/game-{game_id}/{filename}"

# Process the game, save the images and the game to the database
# Returns True if the game was successfully processed, False otherwise
def processGame(game_title, files, answer, hint):
    file_names = []

    try:

        all_file_objects = []

        # create each game based on the images, saving the images in the UPLOADS folder
        for i in range(1, 5):
            file_key = 'image' + str(i)
            file = files[file_key]
            all_file_objects.append(file)
            filename = secure_filename(file.filename)
            file_names.append(filename)

        
        new_game = Game(game_title=game_title, answer=answer, hint=hint, \
                        image1 = file_names[0], image2 = file_names[1], \
                        image3 = file_names[2], image4 = file_names[3], \
                        creator=current_user)
        

        db.session.add(new_game)
        db.session.commit()

        for i,name in enumerate(file_names):
            path  = os.path.join(UPLOAD_FOLDER, "game-" + str(new_game.gameId), name)

            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            all_file_objects[i].seek(0)
            all_file_objects[i].save(path)

        # build the paths for the images
        new_game.image1 = buildPath(new_game.gameId, file_names[0])
        new_game.image2 = buildPath(new_game.gameId, file_names[1])
        new_game.image3 = buildPath(new_game.gameId, file_names[2])
        new_game.image4 = buildPath(new_game.gameId, file_names[3])

        db.session.commit()

        print("The game id is", new_game.gameId)
        print(f"The hint is |{new_game.hint}|")

    except Exception as e:
        print(e)
        return False

    return True
