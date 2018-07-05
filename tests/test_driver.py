# test_drivers

import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class DriversEndpoint(ConfigTestCase):
    """This class represents driver test cases"""

    def test_add_ride(self):
        """Test API can add ride"""
        ride = {"route": "Komarock-Nairobi", "driver": "Chris"}
        res = self.client().post('/api/v3/rides', data=json.dumps(ride), content_type='application/json',
                                 headers=self.driver_header)
        self.assertIn("Ride has been successfully added", str(res.data))
        self.assertEqual(res.status_code, 201)

    def test_get_ride(self):
        """Test API can get ride for driver"""

        res = self.client().get('/api/v3/rides/1', headers=self.user_header)
        self.assertIn("Syo-Nai", str(res.data))
        self.assertEqual(res.status_code, 200)

    def test_add_ride_without_route(self):
        """Test API cannot add ride with route missing"""
        ride = {"driver": "Chris", "time": "9:00"}
        res = self.client().post('/api/v3/rides', data=json.dumps(ride), headers=self.driver_header,
                                 content_type='application/json')
        self.assertIn("Route is not provided Missing required parameter in the JSON body", str(res.data))

    def test_accept_ride(self):
        """Test API driver can accept ride"""

        res = self.client().put('/api/v3/rides/1/accept', headers=self.driver_header)
        self.assertIn("You have confirmed ride taken", str(res.data))
        self.assertEqual(res.status_code, 200)

    def test_get_all_requested_rides(self):
        """Test API can get all requested rides"""

        res = self.client().get('/api/v3/requested', headers=self.driver_header)
        self.assertIn("Ken", str(res.data))
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()