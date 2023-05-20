from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apps import app
from apps.models import Users
from apps.models import db 

class TestRegister(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/register')
        
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.driver.quit()

    def test_register(self):

        ######## UnSuccessful REGISTER ##########
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

        ######## Successful REGISTER ##########
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


        
            