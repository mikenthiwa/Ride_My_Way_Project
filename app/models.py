# models.py
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import psycopg2
from instance.config import config, Config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(150) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(450) NOT NULL,
            is_driver BOOLEAN NULL,
            is_admin BOOLEAN NULL)
        """,

        """ CREATE TABLE rides (
                       ride_id SERIAL PRIMARY KEY,
                       route VARCHAR(155) NOT NULL,
                       driver VARCHAR(150) NOT NULL)
        """,
        """ CREATE TABLE request (
                       id SERIAL PRIMARY KEY,
                       ride_id int NOT NULL,
                       username VARCHAR(155) NOT NULL,
                       pickup_point VARCHAR(150) NOT NULL,
                       time VARCHAR(150) NOT NULL,
                       accept BOOLEAN NULL)
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

class Users:
    """Contains all methods for class users"""

    def __init__(self, username, email, password, is_driver=False, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.is_driver = is_driver
        self.is_admin = is_admin

    def add_users(self):

        """Creates new user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from users where email='{}'".format(self.email))
        cur.execute("SELECT * from users where username='{}'".format(self.username))

        rows = cur.fetchone()
        if rows is None:
            query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                    "('" + self.email + "', '" + self.username + "', '" + self.password + "', '" + '0' + "', '"+ '0' +"')"
            cur.execute(query)
            conn.commit()
            conn.close()

            return {"msg": "You have been successfully added!, log in"}
        return {"msg": 'Account cannot be created!, the email you entered already exists'}, 401

    @staticmethod
    def login(email, password):
        """Login registered users:
        Parameters required email, password"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        cur.execute(
            "SELECT email, user_id, username, password, is_driver, is_admin from users where email='{}'".format(email))
        rows = cur.fetchone()
        if rows is None:
            return {"msg": 'The email you tried to enter does not exist'}, 401
        if not check_password_hash(rows[3], password=password):
            return {"msg": "password do not match"}, 401

        token = jwt.encode(
            {'email': rows[0], 'user_id': rows[1], 'username': rows[2], 'is_driver': rows[4], 'is_admin': rows[5],
             'exp': datetime.datetime.utcnow()}, os.getenv('SECRET_KEY'))

        return {"msg": {"WELCOME TO RIDE_MY_WAY":"copy token to header to  access different functionality", 'token': token.decode('UTF-8')}}

    @staticmethod
    def get_all_user():
        """Get all users"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
            conn.close()
        return output

    @staticmethod
    def get_a_user(email):
        """Get a specific user
        parameters required email"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users;")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email in output:
            return {'email': email, 'username': output[email]['username'], 'is_driver': output[email]['is_driver']}

        return {"msg": "Email is not available"}

    def add_driver(self):
        """Creates new user"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from users where email='{}'".format(self.email))
        rows = cur.fetchone()
        if rows is None:
            query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                    "('" + self.email + "', '" + self.username + "', '" + self.password + "', '" + '1' + "', '" + '0' + "')"
            cur.execute(query)
            conn.commit()
            conn.close()
            return {"msg": "You have been successfully added"}, 201

        return {"msg": 'email is already available'}, 401

    @staticmethod
    def modify_username(email, username):
        """Modify the username of a specific user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return {"msg": "Invalid email"}
        cur.execute("UPDATE users set username = '" + username + "' where email = '" + email + "'")
        conn.commit()

        return {"msg": 'username changed'}

    @staticmethod
    def promote_user(email):
        """Make a user an admin"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return {"msg": 'invalid email'}
        cur.execute("UPDATE users set is_admin = '" + '1' + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": 'User is admin'}

    @staticmethod
    def reset_password(email, password):
        """Parameter required:
        email, password"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return {"msg": 'Invalid email'}
        cur.execute("UPDATE users set password = '" + password + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": "password changed!"}



class Rides:
    """Contains methods for class ride"""

    def __init__(self, route, driver):
        self.route = route
        self.driver = driver

    def add_ride(self):
        """Add new ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from rides where route='{}'".format(self.route))
        rows = cur.fetchone()
        if rows is None:
            query = "INSERT INTO rides (route, driver) VALUES " \
                    "('" + self.route + "', '"+ self.driver + "')"

            cur.execute(query)
            conn.commit()
            conn.close()
            return {"msg": "Ride has been successfully added"}
        return {"msg": "Ride already exists"}

    @staticmethod
    def get_rides():
        """Gets all rides"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            ride_id = row[0]
            output[ride_id] = {"route": row[1],  "driver": row[2]}

        return output


    @staticmethod
    def get_ride(ride_id):
        """Parameter:
        Ride_Id"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"route": row[1], "driver": row[2]}
        if ride_id not in output:
            return {"msg": "ride is not available"}, 404
        ride = output[ride_id]

        return ride

    @staticmethod
    def request_ride(ride_id, username, pickup_point, time):
        """Request a ride
        Parameters: ride_id, username, pickup_point, time"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver from rides")

        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"route": row[1], "driver": row[2]}
        if ride_id not in output:
            return {"msg": "ride is not available"}, 404

        cur.execute("SELECT * from request where username='{}'".format(username))
        rows_request = cur.fetchone()
        if rows_request is None:
            query = "INSERT INTO request (ride_id, username, pickup_point, time, accept) VALUES " \
                    "('" + str(ride_id) + "', '" + username + "', '" + pickup_point + "', '" + time + "', '" + '0'+ "')"
            cur.execute(query)
            conn.commit()
            conn.close()
            return {"msg": "You have successfully requested a ride"}
        return {"msg": "you have already requested"}


    @staticmethod
    def get_all_requested_rides():
        """Driver gets all requested ride"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT id, username, pickup_point, time, accept from request")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            request_id = row[0]
            output[request_id] = {"ride_id": row[0], "username": row[1], "pickup_point": row[3]}

        return output

    @staticmethod
    def get_all_requested_ride_by_id(ride_id):
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from request where ride_id='{}'".format(ride_id))
        rows = cur.fetchone()
        if rows is None:
            return {"msg": "Ride is not available"}
        return {"request_id": rows[0],
                "username": rows[2],
                "pickup_point": rows[3],
                "time": rows[4]}



    @staticmethod
    def accept_ride_taken(ride_id):
        """Parameter: ride_id"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT id, username, pickup_point from request")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            request_id = row[0]
            output[request_id] = {"ride_id": row[0], "username": row[1], "pickup_point": row[2]}
        if ride_id not in output:
            return {"msg": "invalid id"}
        cur.execute("UPDATE request set accept = '" + '1' + "' where id = '" + str(ride_id) + "'")
        conn.commit()

        return {"msg": "You have confirmed ride taken"}

    @staticmethod
    def modify_driver(ride_id, driver):
        """Parameter:
        ride_id, driver"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"driver": row[2]}
        if ride_id not in output:
            return {"msg": "Ride is not available"}, 404
        cur.execute("UPDATE rides set driver = '" + driver + "' where ride_id = '" + str(ride_id) + "'")
        conn.commit()

        return {"msg": "Driver has been successfully modified"}

    @staticmethod
    def modify_route(ride_id, route):
        """Parameter:
        ride_id, route"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]

            output[id] = {"route": row[1]}

        if ride_id in output:
            cur.execute("UPDATE rides set route = '" + route + "' where ride_id = '" + str(ride_id) + "'")
            conn.commit()

            return {"msg": "Route has been successfully modified"}
        return {"msg": "Ride is not available"}, 404


    @staticmethod
    def delete_ride(ride_id):
        """Parameter:
        ride_id"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id from rides")
        rows = cur.fetchall()

        output = []
        for row in rows:
            id = row[0]
            output.append(id)

        if ride_id not in output:
            return {"msg": "Ride is not available"}
        cur.execute("DELETE from rides where ride_id = '" + str(ride_id) + "'")
        conn.commit()
        return {"msg": "Ride has been successfully deleted"}

