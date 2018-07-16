import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class AdminEndpoint(ConfigTestCase):
    """This class represents admin test cases"""

    def test_promote_user(self):
        """Parameter:
        admin token"""

        response = self.client().patch('/api/v3/admin/users/test_user@gmail.com', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User is admin", str(response.data))

        # invalid email
        invalid_response = self.client().patch('/api/v3/admin/users/test@gmail.com', headers=self.admin_header)
        self.assertIn("invalid email", str(invalid_response.data))



    def test_get_users(self):
        """Parameter:
        admin header"""

        res = self.client().get('api/v3/admin/users', headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

    def test_get_a_user(self):
        """Parameter:
        admin header"""
        response = self.client().get('/api/v3/admin/users/test_user@gmail.com', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

        # invalid user
        res = self.client().get('/api/v3/admin/users/chris@gmail.com', headers=self.admin_header)
        self.assertIn("The email you entered does not exist!", str(res.data))



if __name__ == '__main__':
    unittest.main()