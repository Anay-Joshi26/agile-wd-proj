import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import unittest
from config import TestConfig, Config
from flask import Flask
from models import db, User, Game, Attempt, GamePerformance
from flask_bcrypt import Bcrypt
from __init__ import create_app
from generate_fake_data import generate_all_games
from flask_login import login_user, current_user
from api import api, isValidGameTitleOrHint, isValidAnswer
from auth import isValidUsername, isValidPassword

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.bcrypt = Bcrypt(self.app)
        self.app_client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            generate_all_games()
        

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.remove()


    def test_different_passwords_different_hashes(self):
        # test hashing different passwords produces different hashes
        password_1 = "Password123"
        password_2 = "Password456"
        hashed_password_1 = self.bcrypt.generate_password_hash(password_1)
        hashed_password_2 = self.bcrypt.generate_password_hash(password_2)
        self.assertNotEqual(hashed_password_1, hashed_password_2)

    def test_valid_username(self):
        # Test valid usernames
        self.assertTrue(isValidUsername("user123"))
        self.assertTrue(isValidUsername("test_user"))
        self.assertTrue(isValidUsername("user_123"))

    def test_invalid_username_special_characters(self):
        # Test usernames containing special characters
        self.assertFalse(isValidUsername("user!@#"))
        self.assertFalse(isValidUsername("user_@123"))

    def test_invalid_username_whitespace(self):
        # Test usernames containing whitespace
        self.assertFalse(isValidUsername("user 123"))
        self.assertFalse(isValidUsername("user name"))

    def test_valid_password(self):
        # Test valid passwords
        self.assertTrue(isValidPassword("password123"))
        self.assertTrue(isValidPassword("strongPassword!@#"))

    def test_invalid_empty_password(self):
        # Test empty passwords
        self.assertFalse(isValidPassword(""))

    def test_upvote_valid(self):
        # Create a dummy game
        with self.app.app_context():
            user = User(username = 'test', password = 'alsotest')
            game = Game (
                game_title="Lost Treasure Hunt",
                answer="TEST",
                hint="Look for the old palm tree near the cave entrance.",
                image1="treasure_map.jpg",
                image2="pirate_flag.jpg",
                image3="shipwreck.jpg",
                image4="treasure_chest.jpg",
                gameId = 5000,
                creator = user
            )

            db.session.add(user)
            db.session.add(game)
            db.session.commit()

            with self.app.test_request_context():
                login_user(user)

                # Simulate an upvote request

                response = self.app_client.post('/api/upvote/5000')
                data = response.json
                self.assertTrue(data['success'])

    def test_downvote_valid(self):
        # Create a dummy game
        with self.app.app_context():
            user = User(username = 'test', password = 'alsotest')
            game = Game (
                game_title="Lost Treasure Hunt",
                answer="TEST",
                hint="Look for the old palm tree near the cave entrance.",
                image1="treasure_map.jpg",
                image2="pirate_flag.jpg",
                image3="shipwreck.jpg",
                image4="treasure_chest.jpg",
                gameId = 5000,
                creator = user
            )

            db.session.add(user)
            db.session.add(game)
            db.session.commit()

            with self.app.test_request_context():
                login_user(user)

                # Simulate an upvote request

                response = self.app_client.post('/api/downvote/5000')
                data = response.json
                self.assertTrue(data['success'])
    
    def test_upvote_invalid_game(self):
        # Simulate upvoting a non-existing game
        with self.app.app_context():
            user = User(username='test', password='alsotest')
            db.session.add(user)
            db.session.commit()

            with self.app.test_request_context():
                login_user(user)

                response = self.app_client.post('/api/upvote/9999')
                data = response.json
                self.assertFalse(data['success'])

    def test_downvote_invalid_game(self):
        # Simulate downvoting a non-existing game
        with self.app.app_context():
            user = User(username='test', password='alsotest')
            db.session.add(user)
            db.session.commit()

            with self.app.test_request_context():
                login_user(user)

                response = self.app_client.post('/api/downvote/9999')
                data = response.json
                self.assertFalse(data['success'])

    def test_upvote_unauthenticated_user(self):
        # Simulate upvoting without logging in
        response = self.app_client.post('/api/upvote/5000')
        data = response.json
        self.assertFalse(data['success'])

    def test_downvote_unauthenticated_user(self):
        # Simulate downvoting without logging in
        response = self.app_client.post('/api/downvote/5000')
        data = response.json
        self.assertFalse(data['success'])

    def test_upvote_duplicate(self):
        # at the time of writing, the upvote function does not check if the user has already upvoted a game
        # but test driven development is about writing tests before the code, so this should pass in the future
        with self.app.app_context():
            user = User(username='test', password='alsotest')
            game = Game (
                game_title="Lost Treasure Hunt",
                answer="TEST",
                hint="Look for the old palm tree near the cave entrance.",
                image1="treasure_map.jpg",
                image2="pirate_flag.jpg",
                image3="shipwreck.jpg",
                image4="treasure_chest.jpg",
                gameId=5000,
                creator=user
            )

            db.session.add(user)
            db.session.add(game)
            db.session.commit()

            with self.app.test_request_context():
                login_user(user)

                # Simulate an upvote request twice
                self.app_client.post('/api/upvote/5000')
                response = self.app_client.post('/api/upvote/5000')
                data = response.json
                self.assertFalse(data['success'])

    def test_valid_game_title_or_hint(self):
        # Test valid game titles or hints
        self.assertTrue(isValidGameTitleOrHint("Lost Treasure Hunt"))
        self.assertTrue(isValidGameTitleOrHint("The Great Escape"))
        self.assertTrue(isValidGameTitleOrHint("A Journey Through Time"))

    def test_invalid_long_game_title_or_hint(self):
        # Test game titles or hints exceeding maximum length
        self.assertFalse(isValidGameTitleOrHint("This is a very long game title that exceeds the maximum allowed length of 75 characters"))

    def test_empty_game_title_or_hint(self):
        # Test empty game titles or hints
        self.assertFalse(isValidGameTitleOrHint(""))

    def test_valid_answer(self):
        # Test valid answers
        self.assertTrue(isValidAnswer("TEST123"))
        self.assertTrue(isValidAnswer("The Quick Brown Fox"))

    def test_invalid_answer_too_long(self):
        # Test answers exceeding maximum length
        self.assertFalse(isValidAnswer("This answer is too long and exceeds the maximum length allowed by the validation function"))

    def test_invalid_answer_invalid_characters(self):
        # Test answers containing invalid characters
        self.assertFalse(isValidAnswer("Test!@#$"))
        self.assertFalse(isValidAnswer("Test  123"))  # Contains multiple consecutive spaces  


if __name__ == '__main__':
    unittest.main()
