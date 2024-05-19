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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(app_link)

    def tearDown(self):
        # self.driver.close()
        with self.app_context:
            db.session.remove()
            db.drop_all()
            db.session.remove()
            
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

        # first_game = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div/a/h3')
        first_game = self.driver.find_element(By.XPATH, '(//h3)[1]')
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

        self.driver.close()

    def test_5_search_game(self):
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

        search_bar = self.driver.find_element(By.ID, 'srch')
        search_bar.send_keys('te')

        game = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/nav/div[1]/form/div/a[1]'))
        )
        game_title = game.get_attribute('innerText')
        game.click()

        title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/h1'))
        )
        self.assertEqual(title.get_attribute("innerText"), game_title)

        self.driver.close()
    

if __name__ == '__main__':
    unittest.main()
