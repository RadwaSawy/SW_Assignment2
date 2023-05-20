from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apps import app
from apps.models import Users
from apps.models import db 
from werkzeug.security import generate_password_hash
from apps.controller import *

class TestRegister(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/register')
        # create a test user
        with app.app_context():
            new_user = controller.addUser(username = 'olduser' ,email='olduser@example.com', password= generate_password_hash('password', method='sha256'))
        
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.driver.quit()

    def test_register(self):

        ######## UnSuccessful REGISTER ##########
        # Case 1: invalid email
        # Wait for the email field to be present
        wait = WebDriverWait(self.driver, 20)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Enter user information into registration form
        name_field.send_keys('testuser')
        self.driver.find_element(By.NAME, 'email').send_keys('testuserexample.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'register').click()

        # Check that the registration was successful
        self.assertNotEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        # Check that the user was added to the database
        with app.app_context():
            user = Users.query.filter_by(email='testuser@example.com').first()
            self.assertIsNone(user)

        # Case 2: empty email
        # Wait for the email field to be present
        wait = WebDriverWait(self.driver, 20)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Enter user information into registration form
        name_field.send_keys('testuser')
        self.driver.find_element(By.NAME, 'email').send_keys('')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'register').click()

        # Check that the registration was successful
        self.assertNotEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        # Check that the user was added to the database
        with app.app_context():
            user = Users.query.filter_by(username='testuser').first()
            self.assertIsNone(user)
        
        # Case 3: empty username
        # Wait for the email field to be present
        wait = WebDriverWait(self.driver, 20)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Enter user information into registration form
        name_field.send_keys('')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'register').click()

        # Check that the registration was successful
        self.assertNotEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        # Check that the user was added to the database
        with app.app_context():
            user = Users.query.filter_by(email='testuser@example.com').first()
            self.assertIsNone(user)
        
        # Case 4: existed user
        # Wait for the email field to be present
        wait = WebDriverWait(self.driver, 20)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Enter user information into registration form
        name_field.send_keys('olduser')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'register').click()

        # Check that the registration was successful
        self.assertNotEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        
        ######## Successful REGISTER ##########
        # case 5: Registered user 
        # Wait for the email field to be present
        wait = WebDriverWait(self.driver, 20)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Enter user information into registration form
        name_field.send_keys('testuser')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'register').click()

        # Check that the registration was successful
        self.assertEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        # Check that the user was added to the database
        with app.app_context():
            user = Users.query.filter_by(email='testuser@example.com').first()
            self.assertEqual('testuser',user.username)


        
            