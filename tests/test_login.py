import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class LoginEndpoint(ConfigTestCase):
    """This class represents Login test case test cases"""

    def test_login_user_successfully(self):
        """Test user can login successfully"""

        # test passenger login
        test_user = {"email": "test_user@gmail.com", "password": "123456789"}
        res = self.client().post('/api/v3/auth/login', data=json.dumps(test_user), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_invalid_email_login(self):
        """Test API for invalid email"""

        user = {"email": "test2@gmail.com", "password": "123456789"}
        response = self.client().post('/api/v3/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertIn("invalid email", str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_invalid_password(self):
        """Test API for invalid password"""

        user = {"email": "test_user@gmail.com", "password": "123456"}
        response = self.client().post('/api/v3/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertIn("password do not match", str(response.data))
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()