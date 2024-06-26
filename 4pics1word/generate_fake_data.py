from faker import Faker
import requests
import os
from process_game import UPLOAD_FOLDER
import random
from models import db, Game, User, GamePerformance

topics = [
    "Nature",
    "Technology",
    "Adventure",
    "Food",
    "Animals",
    "Travel",
    "Music",
    "Sports",
    "Space",
    "Fantasy",
    "History",
    "Art",
    "Science",
    "Friendship",
    "Love",
    "Mystery",
    "Fashion",
    "Health",
    "Literature",
    "Culture"
]

fake = Faker()

# generate a title of random words
def generate_lorem_title(num_words):
    title_words = [fake.word() for _ in range(num_words)]
    return " ".join(title_words)

# generae a random username and password
# and return them as a tuple
def generate_user():
    username = fake.user_name()
    password = fake.password(length=10)
    return username, password

# unused function/may need to be used later
def download_image(image_url, file_dir):
    response = requests.get(image_url)

    if response.status_code == 200:
        directory = os.path.dirname(file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_dir, "wb") as fp:
            fp.write(response.content)

        #print("Image downloaded successfully.")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

def generate_four_images(topic, game_id):
    print(topic)
    url = f'https://source.unsplash.com/random?{topic}'

    image_paths = []
    for i in range(1,5):
        response = requests.get(url)
        image_url = response.url
        print(image_url)
        image_paths.append(image_url)
        # download_image(url, os.path.join(UPLOAD_FOLDER, f'game-{game_id}/image{i}.jpg'))
        # image_paths.append(f'uploads/game-{game_id}/image{i}.jpg')

    return image_paths


def generate_game(topic, id):
    game_title = generate_lorem_title(7)
    answer = topic
    images = generate_four_images(topic, id)
    return game_title, answer, images

# generate a number of random users using the prevously defined
# helper func
def generate_users(num_users):
    users = []
    for i in range(1, num_users+1):
        username, password = generate_user()
        new_user = User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()
        users.append(new_user)
    return users

        
# main function to generate all the games
# and the users
def generate_all_games():
    users = generate_users(50)

    DUMMY_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dummy_data_images.txt'))

    data = None

    # read the text file with the dummy data
    # each game has a Topic (answer) and 4 API images
    with open(DUMMY_DATA, 'r') as f:
        data = f.read().split('\n')

    num_games = len(data)

    all_games = []
    recent_games_needed = 4  

    for i in range(0, num_games, 5):
        answer = data[i]

        #print(answer)

        game_title = generate_lorem_title(7)

        # Determine the creation date for the game, we need 4 games
        # to be recent for the trending cards
        if recent_games_needed > 0:
            date_created = fake.date_time_between(start_date='-1d', end_date='now')
            recent_games_needed -= 1
        else:
            date_created = fake.date_time_this_year(before_now=True, after_now=False)

        # generate a game with the topic and the images
        # and with random upvotes, from any user
        new_game = Game(
            game_title=game_title,
            answer=answer.upper(),
            image1=data[i+1],
            image2=data[i+2],
            image3=data[i+3],
            image4=data[i+4],
            creator=random.choice(users),
            number_of_upvotes=random.randint(-10, 100),
            date_created=date_created
        )

        all_games.append(new_game)
        
        db.session.add(new_game)
        db.session.commit()

    # generate a random leaderboard for each game
    for game in all_games:
        rg = random.randint(10, 30)
        random.shuffle(users)
        for user in users[:rg]:  
            new_leaderboard = GamePerformance(
                user=user,
                game=game,
                attempts=random.randint(1, 20)
            )

            db.session.add(new_leaderboard)
            db.session.commit()

    





        


