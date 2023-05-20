from apps import app
import unittest
from apps.models import db 
from apps.models import *

class FlaskTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # create a test user
        user = Users(username='testuser', email='testuser@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_logout(self):
        # log in the test user
        response = self.app.post('/login', data=dict(
            Username='testuser',
            Password='password'
        ), follow_redirects=True)

        # check that the status code is 200
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        # log out the user
        response = self.app.get('/logout', follow_redirects=True)

        # check that the status code is 200
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        # check that theuser is redirected to the login page
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()