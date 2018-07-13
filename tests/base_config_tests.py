import unittest
import sys  # fix import errors
import os
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.models import create_tables, Users, Rides



class ConfigTestCase(unittest.TestCase):
    """This class represents the base configurations for all tests"""

    def setUp(self):
        """Define test variables and initialize app"""

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():

            create_tables()

            # Creating user
            user_res = Users(username='test_user', email='test_user@gmail.com', password='123456789')
            user_res.add_users()

            # create driver
            driver_res = Users(username='test_driver', email='test_driver@gmail.com', password='123456789')
            driver_res.add_driver()

            # create admin
            conn = psycopg2.connect(os.getenv('database'))
            cur = conn.cursor()
            hashed_password = generate_password_hash('admin2018', method='sha256')
            query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                    "('admin@admin.com', 'admin', '" + hashed_password + "', '" + '1' + "','" + '1' + "' )"
            cur.execute(query)
            conn.commit()
            conn.close()

            # add ride
            ride_res = Rides("Syo-Nai", "James", "KBZ 481G", "Toyota", 4)
            ride_res.add_ride()

            # request ride
            res = Rides.request_ride(1,username="Ken", pickup_point="TRM", time="5:00")


            test_user_cred = {"email": "test_user@gmail.com", "password": "123456789"}
            test_driver_cred = {"email": "test_driver@gmail.com", "password": "123456789"}
            test_admin_cred = {"email": "admin@admin.com", "password": "admin2018"}

            # login user
            user_response = self.client().post('/api/v3/auth/login', data=json.dumps(test_user_cred),
                                               content_type='application/json')
            driver_response = self.client().post('/api/v3/auth/login', data=json.dumps(test_driver_cred),
                                                 content_type='application/json')
            admin_response = self.client().post('/api/v3/auth/login', data=json.dumps(test_admin_cred),
                                                content_type='application/json')

            # retrieve json
            user_token_dict = json.loads(user_response.get_data(as_text=True))
            driver_token_dict = json.loads(driver_response.get_data(as_text=True))
            admin_token_dict = json.loads(admin_response.get_data(as_text=True))


            user_token = user_token_dict["login successful"]["token"]
            driver_token = driver_token_dict["login successful"]["token"]
            admin_token = admin_token_dict["login successful"]["token"]



            self.user_header = {"Content-Type": "application/json", "x-access-token": user_token}
            self.driver_header = {"Content-Type": "application/json", "x-access-token": driver_token}
            self.admin_header = {"Content-Type": "application/json", "x-access-token": admin_token}


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            conn = psycopg2.connect(os.getenv('database'))
            cur = conn.cursor()
            cur.execute("DROP TABLE users, rides, request")
            conn.commit()

if __name__ == '__main__':
    unittest.main()