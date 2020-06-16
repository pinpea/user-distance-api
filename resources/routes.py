import requests
import json
# from flask import Flask
from flask_restx import Resource, abort, reqparse, inputs

from resources.get_user_details import GetUserDetails
from app import flask_api, api_namespace

DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'



parser = reqparse.RequestParser()

parser.add_argument('city', type=str,default='London', help='returns ', location='args')
parser.add_argument('return_users', type=inputs.boolean, default=False, help='return users as part of the query',location='args')
parser.add_argument('find_users_in_range', type=inputs.boolean, default=True, help='When set to false, only users who are listed as living in a city are counted',location='args')
parser.add_argument('distance', type=float, default=50.0, help='range from a given location to search for users, set find_users_in_range to true to use this parameter', location='args')
parser.add_argument('latitude', type=float, default=51.506 ,help='Latitude of location to perform user search. London by default. set find_users_in_range to true to use this parameter', location='args')
parser.add_argument('longitude', type=float, default=-0.1272 , help='range from a given location to search for users. set find_users_in_range to true to use this parameter', location='args')

@api_namespace.route('/information')
class ApiInfo(Resource):
    def get(self):
        return {'api_overview': 'todo'}

@api_namespace.route('/get_number_of_users_in_range/')
class GetUsersGeneric(Resource):
    @api_namespace.expect(parser)
    def get(self):

        try: 
            args = parser.parse_args()
            requested_lat_long = (args['latitude'], args['longitude'])
            GUD = GetUserDetails(DATA_ROOT_URL)
             
            users_near_city = (GUD.get_all_users_near_city(args['distance'], args['city'], args['find_users_in_range'], requested_lat_long)).to_dict(orient='records')

            if args['return_users']==False:
                return {'number_of_users': len(users_near_city)}
            else: 
                return {'number_of_users': len(users_near_city), 'users:' : users_near_city}

        except KeyError as e:
            api_namespace.abort(400, str(e), status = "Bad Request", statusCode = "400")
        except Exception as e:
            api_namespace.abort(500, str(e), status = "Could not retrieve information", statusCode = "500")

@api_namespace.route('/get_total_number_of_users',doc={"description": "Alias for /my-resource/<id>"})
# @api_namespace.doc(params={'': 'Search for all users within this distance of a location, default is 50miles (location given by following latitude,longitude).'})
class ApiInfo(Resource):
    def get(self):
        GUD = GetUserDetails(DATA_ROOT_URL)
        total_number_of_users = GUD.get_total_num_of_users()
        return {'total_number_of_users': total_number_of_users}

