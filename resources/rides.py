from flask_restplus import Resource, Namespace, reqparse, fields
from app.models import Rides
from resources.auth import token_required
from instance.config import Config
from flask import request
import jwt


api = Namespace("Rides",  description="Passenger related operations")

request_model = api.model('Request Model', {"pickup_point": fields.String,
                                            "time": fields.String})


class RideList(Resource):
    """Contain GET methods"""

    @api.doc(security='apikey')
    @token_required
    def get(self):

        """Get all rides """
        response = Rides.get_rides()
        return response


class Ride(Resource):
    """Contains GET method"""

    @api.doc(security='apikey')
    @token_required
    def get(self, ride_id):
        """get a ride(passenger)"""

        response = Rides.get_ride(ride_id=ride_id)
        return response


class RequestRide(Resource):
    """Contain PATCH method"""

    @api.expect(request_model)
    @api.doc(security='apikey')
    @token_required
    def post(self, ride_id):
        """Request ride: ride_id"""
        parser = reqparse.RequestParser()

        parser.add_argument('pickup_point', required=True, type=str, help='Pickup_point is required', location=['json'])
        parser.add_argument('time', required=True, type=str, help='Pickup_point is required', location=['json'])
        token = request.headers['x-access-token']
        data = jwt.decode(token, Config.SECRET)
        driver_name = data['username']
        args = parser.parse_args()
        pickup_point = args['pickup_point']
        time = args['time']

        res = Rides.request_ride(ride_id=ride_id, username=driver_name, pickup_point=pickup_point, time=time)
        return res


api.add_resource(RideList, '/rides', endpoint='ridelist')
api.add_resource(Ride, '/rides/<int:ride_id>')
api.add_resource(RequestRide, '/rides/<int:ride_id>/requests')
