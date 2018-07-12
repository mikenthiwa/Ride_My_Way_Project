# drivers.py

from flask_restplus import Resource, Namespace, reqparse, fields
from app.models import Rides
from resources.auth import driver_required
from instance.config import Config
from flask import request
import jwt



api = Namespace("Driver",  description="Driver related operations")
ride_model = api.model("Ride", {'route': fields.String,
                                'registration number': fields.String,
                                'vehicle model': fields.String,
                                'vehicle capacity': fields.Integer})


class DriverRide(Resource):
    """Contains GET POST method"""

    @api.expect(ride_model)
    @api.doc(security='apikey')
    @driver_required
    def post(self):
        """Add a ride endpoint"""
        parser = reqparse.RequestParser()
        parser.add_argument('route', type=str, required=True, help="Route is not provided", location=['json'])
        parser.add_argument('registration_number', type=str, required=True, help="Registration number is not provided", location=['json'])
        parser.add_argument('vehicle_model', type=str, required=True, help="Vehicle model is not provided", location=['json'])
        parser.add_argument('vehicle_capacity', type=int, required=True, help="vehicle capacity is not provided", location=['json'])

        token = request.headers['x-access-token']
        data = jwt.decode(token, Config.SECRET)
        driver = data['username']

        args = parser.parse_args()
        res = Rides(args['route'], driver=driver, registration_plate=args['registration_number'],
                    vehicle_model=args['vehicle_model'], vehicle_capacity=args['vehicle_capacity'])
        return res.add_ride(), 201

class ModifyRide(Resource):
    "Contain GET PUT method"

    parser = reqparse.RequestParser()
    parser.add_argument('route', type=str, required=False, location=['json'])
    parser.add_argument("driver", type=str, required=False, location=['json'])

    @api.expect(ride_model)
    @api.doc(security='apikey')
    @driver_required
    def put(self, ride_id):
        """Modifying ride detail
        Parameters ride_id"""

        args = self.parser.parse_args()
        route = args['route']
        driver = args['driver']

        if route:
            res = Rides.modify_route(ride_id=ride_id, route=route)
            return res

        elif driver:
            res = Rides.modify_driver(ride_id=ride_id, driver=driver)
            return res

        else:
            return {"msg": "At least one field is required"}

    @api.doc(security='apikey')
    @driver_required
    def delete(self, ride_id):
        res = Rides.delete_ride(ride_id=ride_id)
        return res


class RequestedRide(Resource):
    """Contain GET method"""

    @api.doc(security='apikey')
    @driver_required
    def get(self):
        """Get all requested ride"""
        res = Rides.get_all_requested_rides()
        return res

class RequestRidebyId(Resource):
    """Contains get method"""

    @api.doc(security='apikey')
    @driver_required
    def get(self, ride_id):
        """Get requested ride
        Parameter ride_id"""
        res = Rides.get_all_requested_ride_by_id(ride_id=ride_id)
        return res


class AcceptRide(Resource):

    """Contain PUT method"""

    @api.doc(security='apikey')
    # @driver_required
    def put(self, ride_id):
        """Parameter: ride_id"""

        res = Rides.accept_ride_taken(ride_id=ride_id)
        return res

api.add_resource(DriverRide, '/driver/rides')
api.add_resource(AcceptRide, '/driver/rides/<int:ride_id>/accept')
api.add_resource(ModifyRide, '/driver/rides/<int:ride_id>')
api.add_resource(RequestedRide, '/requested', endpoint='requested')
api.add_resource(RequestRidebyId, '/driver/rides/<int:ride_id>/requests')
