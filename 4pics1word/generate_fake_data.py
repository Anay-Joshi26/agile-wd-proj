from faker import Faker
import requests
import os
from process_game import UPLOAD_FOLDER
import random
from models import db, Game, User

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

def generate_lorem_title(num_words):
    title_words = [fake.word() for _ in range(num_words)]
    return " ".join(title_words)


def generate_user():
    username = fake.user_name()
    password = fake.password(length=10)
    return username, password

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

    print(url)

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
    game_title = generate_lorem_title(6)
    answer = topic
    images = generate_four_images(topic, id)
    return game_title, answer, images

def generate_users(num_users):
    users = []
    for i in range(1, num_users+1):
        username, password = generate_user()
        new_user = User(username = username, password = password)
        
        db.session.add(new_user)
        db.session.commit()
        users.append(new_user)
    return users

        

def generate_all_games(num_games):
    users = generate_users(20)
    for i in range(1, num_games+1):
        game_title, answer, images = generate_game(random.choice(topics),i)
        new_game = Game(game_title=game_title, answer=answer, image1=images[0], image2=images[1], image3=images[2], image4=images[3],\
                        creator = random.choice(users))
        
        db.session.add(new_game)
        db.session.commit()




        


