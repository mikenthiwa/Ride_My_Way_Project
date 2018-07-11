from flask_restplus import Resource, Namespace
from app.models import Users
from resources.auth import admin_required



api = Namespace('Admin', description='Admin related operation')


class AdminUserList(Resource):
    """Contains GET method for Admin Endpoint"""

    @api.doc(security='apikey')
    @admin_required
    def get(self):
        """get all users"""
        res = Users.get_all_user()
        return res


class AdminUser(Resource):
    """Contain
    GET PUT PATCH"""

    @staticmethod
    @api.doc(security='apikey')
    @admin_required
    def get(email):
        """Get one users by id"""
        response = Users.get_a_user(email=email)
        return response



    @api.doc(security='apikey')
    @admin_required
    def patch(self, email):
        """Update user to admin"""
        response = Users.promote_user(email=email)
        return response


api.add_resource(AdminUserList, '/admin/users', endpoint='admin')
api.add_resource(AdminUser, '/admin/users/<string:email>')