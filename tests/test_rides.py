import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class RidesEndpoint(ConfigTestCase):
    """This class represents rides test cases"""

    def test_get_all_rides(self):
        """Test API can get all rides"""

        res = self.client().get('/api/v3/rides', headers=self.user_header)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Syo-Nai", str(res.data))

    def test_get_invalid_ride(self):
        """Test API for invalid ride"""

        res = self.client().get('/api/v3/rides/105', headers=self.user_header)
        self.assertIn("ride is not available", str(res.data))
        self.assertEqual(res.status_code, 404)

    def test_request_ride(self):
        """Test API can request a ride"""

        data = {"pickup_point": "syo", "time": "8:00"}
        res = self.client().post('/api/v3/rides/2/request', data=json.dumps(data),
                                 content_type='application/json', headers=self.user_header)
        self.assertIn("You have successfully requested a ride", str(res.data))
        self.assertEqual(res.status_code, 201)



if __name__ == '__main__':
    unittest.main()