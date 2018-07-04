# models.py
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import request
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
                       driver VARCHAR(150) NOT NULL,
                       time VARCHAR(150) NOT NULL)
        """,
        """ CREATE TABLE request (
                       id SERIAL PRIMARY KEY,
                       username VARCHAR(155) NOT NULL,
                       pickup_point VARCHAR(150) NOT NULL,
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

            return {"msg": "You have been successfully added"}
        return {"msg": 'email is already available'}, 401

    @staticmethod
    def login(email, password):
        """Login registered users"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        cur.execute(
            "SELECT email, user_id, username, password, is_driver, is_admin from users where email='{}'".format(email))
        rows = cur.fetchone()
        if rows is None:
            return {"msg": 'invalid email'}, 401
        if not check_password_hash(rows[3], password=password):
            return {"msg": "password do not match"}, 401

        token = jwt.encode(
            {'email': rows[0], 'user_id': rows[1], 'username': rows[2], 'is_driver': rows[4], 'is_admin': rows[5],
             'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=12)}, os.getenv('SECRET_KEY'))

        return {'token': token.decode('UTF-8')}

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
        """Get a specific user"""

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
            return {"msg": 'email is already available'}
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
            return {"msg": 'email is already available'}
        cur.execute("UPDATE users set is_admin = '" + '1' + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": 'user is admin!'}

    @staticmethod
    def reset_password(email, password):

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return {"msg": 'user is admin!'}
        cur.execute("UPDATE users set password = '" + password + "' where email = '" + email + "'")
        conn.commit()



class Rides:
    """Contains methods for class ride"""

    def __init__(self, route, time, driver):
        self.route = route
        self.driver = driver
        self.time = time


    def add_ride(self):
        """Add new ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        query = "INSERT INTO rides (route, driver, time) VALUES " \
                "('" + self.route + "', '"+ self.driver + "', '" + self.time + "')"

        cur.execute(query)
        conn.commit()
        conn.close()
        return {"msg": "Ride has been successfully added"}


    @staticmethod
    def get_rides(ride_id):
        """Gets all rides"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            ride_id = row[0]
            output[ride_id] = {"route": row[1], "time": row[2], "driver": row[3]}
        if ride_id not in output:
            return {"msg": "invalid id"}, 404
        return output

    @staticmethod
    def request_ride(username, pickup_point):
        """Request a ride"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        query = "INSERT INTO request (username, pickup_point) VALUES " \
                "('" + username + "', '" + pickup_point + "')"
        cur.execute(query)
        conn.commit()
        conn.close()
        return {"msg": "You have successfully requested a ride"}

    @staticmethod
    def accept_ride_taken(ride_id):
        """Driver can accept a ride selected"""

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

