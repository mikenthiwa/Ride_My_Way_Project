# signup_login.py

from flask_restplus import Namespace, Resource, fields, reqparse, inputs
from app.models import Users



api = Namespace('SignUp and Login', description='Sign-up and Login')

model_register = api.model('Sign up', {'username': fields.String(required=True),
                                       'email': fields.String(required=True),
                                       'password': fields.String(required=True),
                                       'is_driver': fields.Boolean(default=False)})

# model for login
model_login = api.model('Login', {'email': fields.String,
                                  'password': fields.String})


class Register(Resource):
    """class contain POST method"""
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="No username provided", location=['json'])

    parser.add_argument('email', required=True, help="No email provided", location=['json'],
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    parser.add_argument('password', required=True, help="No password provided", location=['json'])

    parser.add_argument('is_driver', required=False, location=['json'])

    @api.expect(model_register)
    def post(self):
        """Register user"""

        args = self.parser.parse_args(strict=True)

        username = args['username']
        email = args['email']
        password = args['password']
        driver = args['is_driver']



        if username == "" or email == "" or password == "" or driver == "":
            return {"msg": "Field cannot be empty"}

        if driver == "True":
            driver_res = Users(username=username, email=email, password=password, is_driver=True)
            return driver_res.add_driver()
        user_res = Users(username=username, email=email, password=password)
        return user_res.add_users(), 201



class Login(Resource):
    """class contain post method"""
    req_data = reqparse.RequestParser()
    req_data.add_argument('email', required=True, help='email required', location=['json'],
                          type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    req_data.add_argument('password', required=True, help='password required', location=['json'])


    @api.expect(model_login)
    def post(self):
        """Login user"""
        args = self.req_data.parse_args(strict=True)
        email = args['email']
        password = args['password']
        res = Users.login(email=email, password=password)
        return res


api.add_resource(Register, '/auth/signup', endpoint='register')
api.add_resource(Login, '/auth/login', endpoint='login')
