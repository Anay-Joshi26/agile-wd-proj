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
from main import app
from auth import isValidUsername, isValidPassword

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time


# class TestApp(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(TestConfig)
#         self.bcrypt = Bcrypt(self.app)
#         self.app_client = self.app.test_client()

#         with self.app.app_context():
#             db.create_all()
#             generate_all_games()
        

#     def tearDown(self):
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all()
#             db.session.remove()


#     def test_different_passwords_different_hashes(self):
#         # test hashing different passwords produces different hashes
#         password_1 = "Password123"
#         password_2 = "Password456"
#         hashed_password_1 = self.bcrypt.generate_password_hash(password_1)
#         hashed_password_2 = self.bcrypt.generate_password_hash(password_2)
#         self.assertNotEqual(hashed_password_1, hashed_password_2)

#     def test_valid_username(self):
#         # Test valid usernames
#         self.assertTrue(isValidUsername("user123"))
#         self.assertTrue(isValidUsername("test_user"))
#         self.assertTrue(isValidUsername("user_123"))

#     def test_invalid_username_special_characters(self):
#         # Test usernames containing special characters
#         self.assertFalse(isValidUsername("user!@#"))
#         self.assertFalse(isValidUsername("user_@123"))

#     def test_invalid_username_whitespace(self):
#         # Test usernames containing whitespace
#         self.assertFalse(isValidUsername("user 123"))
#         self.assertFalse(isValidUsername("user name"))

#     def test_valid_password(self):
#         # Test valid passwords
#         self.assertTrue(isValidPassword("password123"))
#         self.assertTrue(isValidPassword("strongPassword!@#"))

#     def test_invalid_empty_password(self):
#         # Test empty passwords
#         self.assertFalse(isValidPassword(""))

#     def test_upvote_valid(self):
#         # Create a dummy game
#         with self.app.app_context():
#             user = User(username = 'test', password = 'alsotest')
#             game = Game (
#                 game_title="Lost Treasure Hunt",
#                 answer="TEST",
#                 hint="Look for the old palm tree near the cave entrance.",
#                 image1="treasure_map.jpg",
#                 image2="pirate_flag.jpg",
#                 image3="shipwreck.jpg",
#                 image4="treasure_chest.jpg",
#                 gameId = 5000,
#                 creator = user
#             )

#             db.session.add(user)
#             db.session.add(game)
#             db.session.commit()

#             with self.app.test_request_context():
#                 login_user(user)

#                 # Simulate an upvote request

#                 response = self.app_client.post('/api/upvote/5000')
#                 data = response.json
#                 self.assertTrue(data['success'])

#     def test_downvote_valid(self):
#         # Create a dummy game
#         with self.app.app_context():
#             user = User(username = 'test', password = 'alsotest')
#             game = Game (
#                 game_title="Lost Treasure Hunt",
#                 answer="TEST",
#                 hint="Look for the old palm tree near the cave entrance.",
#                 image1="treasure_map.jpg",
#                 image2="pirate_flag.jpg",
#                 image3="shipwreck.jpg",
#                 image4="treasure_chest.jpg",
#                 gameId = 5000,
#                 creator = user
#             )

#             db.session.add(user)
#             db.session.add(game)
#             db.session.commit()

#             with self.app.test_request_context():
#                 login_user(user)

#                 # Simulate an upvote request

#                 response = self.app_client.post('/api/downvote/5000')
#                 data = response.json
#                 self.assertTrue(data['success'])
    
#     def test_upvote_invalid_game(self):
#         # Simulate upvoting a non-existing game
#         with self.app.app_context():
#             user = User(username='test', password='alsotest')
#             db.session.add(user)
#             db.session.commit()

#             with self.app.test_request_context():
#                 login_user(user)

#                 response = self.app_client.post('/api/upvote/9999')
#                 data = response.json
#                 self.assertFalse(data['success'])

#     def test_downvote_invalid_game(self):
#         # Simulate downvoting a non-existing game
#         with self.app.app_context():
#             user = User(username='test', password='alsotest')
#             db.session.add(user)
#             db.session.commit()

#             with self.app.test_request_context():
#                 login_user(user)

#                 response = self.app_client.post('/api/downvote/9999')
#                 data = response.json
#                 self.assertFalse(data['success'])

#     def test_upvote_unauthenticated_user(self):
#         # Simulate upvoting without logging in
#         response = self.app_client.post('/api/upvote/5000')
#         data = response.json
#         self.assertFalse(data['success'])

#     def test_downvote_unauthenticated_user(self):
#         # Simulate downvoting without logging in
#         response = self.app_client.post('/api/downvote/5000')
#         data = response.json
#         self.assertFalse(data['success'])

#     def test_upvote_duplicate(self):
#         # at the time of writing, the upvote function does not check if the user has already upvoted a game
#         # but test driven development is about writing tests before the code, so this should pass in the future
#         with self.app.app_context():
#             user = User(username='test', password='alsotest')
#             game = Game (
#                 game_title="Lost Treasure Hunt",
#                 answer="TEST",
#                 hint="Look for the old palm tree near the cave entrance.",
#                 image1="treasure_map.jpg",
#                 image2="pirate_flag.jpg",
#                 image3="shipwreck.jpg",
#                 image4="treasure_chest.jpg",
#                 gameId=5000,
#                 creator=user
#             )

#             db.session.add(user)
#             db.session.add(game)
#             db.session.commit()

#             with self.app.test_request_context():
#                 login_user(user)

#                 # Simulate an upvote request twice
#                 self.app_client.post('/api/upvote/5000')
#                 response = self.app_client.post('/api/upvote/5000')
#                 data = response.json
#                 self.assertFalse(data['success'])

#     def test_valid_game_title_or_hint(self):
#         # Test valid game titles or hints
#         self.assertTrue(isValidGameTitleOrHint("Lost Treasure Hunt"))
#         self.assertTrue(isValidGameTitleOrHint("The Great Escape"))
#         self.assertTrue(isValidGameTitleOrHint("A Journey Through Time"))

#     def test_invalid_long_game_title_or_hint(self):
#         # Test game titles or hints exceeding maximum length
#         self.assertFalse(isValidGameTitleOrHint("This is a very long game title that exceeds the maximum allowed length of 75 characters"))

#     def test_empty_game_title_or_hint(self):
#         # Test empty game titles or hints
#         self.assertFalse(isValidGameTitleOrHint(""))

#     def test_valid_answer(self):
#         # Test valid answers
#         self.assertTrue(isValidAnswer("TEST123"))
#         self.assertTrue(isValidAnswer("The Quick Brown Fox"))

#     def test_invalid_answer_too_long(self):
#         # Test answers exceeding maximum length
#         self.assertFalse(isValidAnswer("This answer is too long and exceeds the maximum length allowed by the validation function"))

#     def test_invalid_answer_invalid_characters(self):
#         # Test answers containing invalid characters
#         self.assertFalse(isValidAnswer("Test!@#$"))
#         self.assertFalse(isValidAnswer("Test  123"))  # Contains multiple consecutive spaces


app_link = "http://127.0.0.1:5000"

class TestWebApp(unittest.TestCase):
        
    def setUp(self):
        testApp = create_app(Config)
        self.app_context = testApp.app_context()
        self.app_context.push()

        with self.app_context:        
            db.create_all()
            generate_all_games()

        options = Options()
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(app_link)

    def tearDown(self):
        # self.driver.close()
        with self.app_context:
            db.session.remove()
            db.drop_all()
            
        self.app_context.pop()

    def test_1_register(self):
        self.driver.implicitly_wait(5)
        register = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[4]/a')
        register.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-register'))
        )

        password_field = self.driver.find_element(By.ID, 'password-register')
        password_confirm_field = self.driver.find_element(By.ID, 'password-confirm-register')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_confirm_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        # password_confirm_field.send_keys(Keys.RETURN)
        register_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
        register_button.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-login'))
        )

        new_user = User.query.filter_by(username="seltestrun").first()
        # self.assertEqual(len(new_user), 1)
        self.assertEqual(new_user.username, 'seltestrun')

        self.driver.close()

    def test_2_login(self):
        register = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[4]/a')
        register.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-register'))
        )

        password_field = self.driver.find_element(By.ID, 'password-register')
        password_confirm_field = self.driver.find_element(By.ID, 'password-confirm-register')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_confirm_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        # password_confirm_field.send_keys(Keys.RETURN)
        register_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
        register_button.click()

        # login = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[3]/a')
        # login.click()

        # username_field = self.driver.find_element(By.ID, 'username-login')

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-login'))
        )

        password_field = self.driver.find_element(By.ID, 'password-login')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/form/button')
        login_button.click()

        first_image = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'card-img-top'))
        )

        self.assertEqual(self.driver.current_url, app_link+"/challenges")
        self.driver.close()


    def test_3_create_game(self):
        self.driver.implicitly_wait(5)
        register = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[4]/a')
        register.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-register'))
        )

        password_field = self.driver.find_element(By.ID, 'password-register')
        password_confirm_field = self.driver.find_element(By.ID, 'password-confirm-register')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_confirm_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        register_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
        register_button.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-login'))
        )

        password_field = self.driver.find_element(By.ID, 'password-login')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/form/button')
        login_button.click()

        first_image = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'card-img-top'))
        )

        create_game = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[1]/a')
        create_game.click()

        game_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'game-title-input'))
        )

        image1 = self.driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[1]/div/input')
        image2 = self.driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[2]/div/input')
        image3 = self.driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[3]/div/input')
        image4 = self.driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[4]/div/input')

        phrase = self.driver.find_element(By.ID, 'word-input')

        make_hint_available = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/span')
        make_hint_available.click()

        hint = self.driver.find_element(By.XPATH, '/html/body/form/div[6]/input')

        image1.send_keys(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'assets', 'nature-1.jpg')))
        image2.send_keys(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'assets', 'nature-2.jpg')))
        image3.send_keys(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'assets', 'nature-3.jpg')))
        image4.send_keys(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'assets', 'nature-4.jpg')))

        game_title.send_keys('TEST')
        phrase.send_keys('TEST')
        hint.send_keys('TEST')

        submit_game_button = self.driver.find_element(By.ID, 'submit-upload-game')
        submit_game_button.click()

        first_image = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'card-img-top'))
        )

        newly_made_game = Game.query.order_by(Game.date_created.desc()).first()

        self.assertEqual(self.driver.current_url, app_link+"/challenges")
        self.assertEqual(newly_made_game.game_title, 'TEST')
        self.assertEqual(newly_made_game.answer, 'TEST')
        self.assertEqual(newly_made_game.hint, 'TEST')

        self.driver.close()

    def test_4_play_game(self):
        self.driver.implicitly_wait(5)
        register = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[4]/a')
        register.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-register'))
        )

        password_field = self.driver.find_element(By.ID, 'password-register')
        password_confirm_field = self.driver.find_element(By.ID, 'password-confirm-register')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_confirm_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        register_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
        register_button.click()

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username-login'))
        )

        password_field = self.driver.find_element(By.ID, 'password-login')
        self.driver.implicitly_wait(5)

        username_field.send_keys("seltestrun")
        self.driver.implicitly_wait(5)
        password_field.send_keys("seltestrun")
        self.driver.implicitly_wait(10)

        login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/form/button')
        login_button.click()

        first_image = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'card-img-top'))
        )

        first_game = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div/a/h3')
        first_game.click()

        play_game = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div[2]/a')
        play_game.click()

        guess = ['h','e','a','l','t','h']
        for id,letter in  enumerate(guess):
            letter_input = self.driver.find_element(By.ID, f'input{id}')
            letter_input.send_keys(letter)

        make_guess = self.driver.find_element(By.ID, 'make-guess')
        make_guess.click()

        go_back = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/a'))
        )

        attempt = Attempt.query.order_by(Attempt.attempt_id.desc()).first()
        performance = GamePerformance.query.order_by(GamePerformance.id.desc()).first()
        
        self.assertEqual(attempt.attempts, 1)
        self.assertEqual(attempt.guess, "HEALTH")
        self.assertEqual(attempt.player.username, performance.user.username)


    # def setUp(self):
        # self.app = create_app(TestConfig)
        # self.bcrypt = Bcrypt(self.app)
        # self.app_client = self.app.test_client()

        # with self.app.app_context():
        #     db.create_all()
        #     generate_all_games()

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # # self.options = webdriver.ChromeOptions()
        # # self.options.add_argument('--headless')
        # # self.options.add_argument('--no-sandbox')
        # # self.options.add_argument('--disable-dev-shm-usage')
        # options = Options()
        # options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # print("created driver")
        # #self.driver.implicitly_wait(10)  # Set implicit wait time to handle dynamic elements

    # def tearDown(self):
        # self.driver.close()
        # self.driver.quit()

        # with self.app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        #     db.session.remove()


    # def test_login_valid_credentials(self):
        # Test logging in with valid credentials
        # self.driver.get(app_link)

        # # login = self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[3]/a')
        # # login.click()

        # try:
        #     # Use WebDriverWait to wait until the element is clickable
        #     # wait = WebDriverWait(self.driver, 10)
        #     # element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Login')))
        #     element = self.driver.find_element(By.ID, 'loginModal')
        #     # self.driver.implicitly_wait(10)
        #     # Click the element
        #     # element.click()
        #     # wait = WebDriverWait(self.driver, 10)
        #     ActionChains(self.driver).move_to_element(element).click(element).perform()

        #     print("Element clicked successfully.")
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        # # finally:
        # #     # Close the WebDriver
        # #     # self.driver.quit()

        # username_field = self.driver.find_element(By.ID, 'username-login')

        # # password_field = self.driver.find_element(By.ID, 'password-login')
        
        # print('USERNAME FIELD', username_field)

        # if username_field.is_displayed():
        #     print("Username Element is visible.")    
        # else:
        #     print("WASNT VISIBLE")

        # if password_field.is_displayed():
        #     print("Password Element is visible.")
        # else:
        #     print("WASNT VISIBLE")

        # username_field.send_keys("TEST")
        # password_field.send_keys("TEST")
        # password_field.send_keys(Keys.RETURN)

        # self.assertTrue(User.query.filter_by(username="TEST").first() is not None)
        
        # # Assert that login was successful by checking if redirected to the home page

        # self.assertEqual(self.driver.current_url, app_link)

    # def test_login_invalid_credentials(self):
    #     # Test logging in with invalid credentials
    #     self.driver.get("http://yourwebapp.com/login")
    #     username_field = self.driver.find_element_by_name("username")
    #     password_field = self.driver.find_element_by_name("password")
    #     username_field.send_keys("invalid_username")
    #     password_field.send_keys("invalid_password")
    #     password_field.send_keys(Keys.RETURN)
    #     # Assert that login failed by checking if error message is displayed
    #     error_message = self.driver.find_element_by_class_name("error-message").text
    #     self.assertEqual(error_message, "Invalid username or password.")
    

    

if __name__ == '__main__':
    unittest.main()
