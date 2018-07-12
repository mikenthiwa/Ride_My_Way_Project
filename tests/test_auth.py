import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class Auth(ConfigTestCase):
    """This class represents auth test cases"""

    def test_missing_token(self):
        """Test API for missing token"""

        # missing driver token
        ride = {"route": "Komarock-Nairobi", "driver": "Chris"}
        response = self.client().post('/api/v3/driver/rides', data=json.dumps(ride), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Please sign-up and login", str(response.data))

        # missing user token
        res = self.client().get('/api/v3/rides/1', content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn("Please sign-up and login", str(res.data))

        # missing admin token
        admin_res = self.client().get('api/v3/admin/users')
        self.assertEqual(admin_res.status_code, 401)
        self.assertIn("Please sign-up and login", str(admin_res.data))

    def test_invalid_token(self):
        """Test API for invalid token"""

        ride = {"route": "Komarock-Nairobi", "driver": "Chris"}
        driver_header = {"Content-Type": "application/json", "x-access-token": "qwertyuioasdfghj"}
        response = self.client().post('/api/v3/driver/rides', data=json.dumps(ride), content_type='application/json', headers=driver_header)
        self.assertEqual(response.status_code, 401)
        self.assertIn("kindly provide a valid token in the header", str(response.data))


        # invalid user token token
        res = self.client().get('/api/v3/rides/1', content_type='application/json', headers=driver_header)
        self.assertEqual(response.status_code, 401)
        self.assertIn("kindly provide a valid token in the header", str(res.data))

        # invalid admin token
        admin_res = self.client().get('api/v3/admin/users', content_type='application/json', headers=driver_header)
        self.assertEqual(admin_res.status_code, 401)
        self.assertIn("kindly provide a valid token in the header", str(admin_res.data))