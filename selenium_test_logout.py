from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apps import app
import unittest
from apps.models import db 
from apps.models import *
from apps.controller import *
from werkzeug.security import generate_password_hash


class TestLogout(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

        # create a test user
        with app.app_context():
            new_user = controller.addUser(username = 'testuser_log' ,email='testuser_log@example.com', password= generate_password_hash('password', method='sha256'))
            

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.driver.quit()

    def test_logout(self):
        # log in the test user
        wait = WebDriverWait(self.driver, 30)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'Username')))
        name_field.send_keys('testuser_log')
        self.driver.find_element(By.NAME, 'Password').send_keys('password')
        self.driver.find_element(By.NAME, 'login').click()

        # check that the user is redirected to the main dashboard
        self.assertEqual(self.driver.current_url, 'http://localhost:5000/main-dashboard.html')

        # log out the userand check that they are redirected to the login page
        self.driver.find_element(By.ID, 'logout-link').click()
        self.assertEqual(self.driver.current_url, 'http://localhost:5000/login')

        