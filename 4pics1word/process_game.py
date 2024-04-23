from werkzeug.utils import secure_filename
import os
from models import db, User, Game
from flask_login import current_user
import re

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def isValidGameTitleOrHint(game_title):
    return len(game_title) <= 75 and len(game_title) > 0

def isValidAnswer(answer):
    return re.match(r"^(?!.*\s\s)(?!^\s)[a-zA-Z0-9\s]{1,24}$", answer)

def buildPath(game_id, filename):
    return f"/uploads/game-{game_id}/{filename}"


def processGame(game_title, files, answer, hint):
    file_names = []

    try:

        for i in range(1, 5):
            file_key = 'image' + str(i)
            file = files[file_key]
            filename = secure_filename(file.filename)
            file_names.append(filename)

        
        new_game = Game(game_title=game_title, answer=answer, hint=hint, \
                        image1 = file_names[0], image2 = file_names[1], \
                        image3 = file_names[2], image4 = file_names[3], \
                        creator=current_user)
        

        db.session.add(new_game)
        db.session.commit()

        for name in file_names:
            path  = os.path.join(UPLOAD_FOLDER, "game-" + str(new_game.gameId), name)

            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            file.seek(0)
            file.save(path)

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
