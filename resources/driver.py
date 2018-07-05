# drivers.py

from flask_restplus import Resource, Namespace, reqparse, fields
from app.models import Rides
from resources.auth import driver_required



api = Namespace("Driver",  description="Driver related operations")
ride_model = api.model("Ride", {'route': fields.String,
                                'driver': fields.String})


class DriverRide(Resource):
    """Contains GET POST method"""

    @api.expect(ride_model)
    @api.doc(security='apikey')
    @driver_required
    def post(self):
        """Add a ride endpoint"""
        parser = reqparse.RequestParser()
        parser.add_argument('route', type=str, required=True, help="Route is not provided", location=['json'])
        parser.add_argument("driver", type=str, required=True, help="Time is not provided", location=['json'])

        args = parser.parse_args()
        res = Rides(args['route'], args['driver'])
        return res.add_ride(), 201

class RequestedRide(Resource):
    """Contain GET method"""

    # @driver_required
    def get(self):
        res = Rides.get_all_requested_rides()
        return res

class AcceptRide(Resource):

    """Contain PATCH method"""

    @api.doc(security='apikey')
    # @driver_required
    def put(self, ride_id):
        """Driver accepts ride taken by passenger"""

        res = Rides.accept_ride_taken(ride_id=ride_id)
        return res

api.add_resource(DriverRide, '/rides')
api.add_resource(AcceptRide, '/rides/<int:ride_id>/accept')
api.add_resource(RequestedRide, '/requested', endpoint='requested')
