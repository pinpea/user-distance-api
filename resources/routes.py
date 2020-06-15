import requests
import json
# from flask import Flask
from flask_restx import Resource

from resources.get_user_details import GetUserDetails
from app import flask_api

DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'


@flask_api.route('/hello')
class CheckApi(Resource):
    def get(self):
        return {'hello': 'world'}


@flask_api.route('/get_users_in_london')
class GetKeys(Resource):
    def get(self):
        GUD = GetUserDetails(DATA_ROOT_URL)
        london_users = GUD.get_users_in_requested_city(input_city='London')
        return {'users_listed_near_london': london_users.to_json(orient='table')}


@ flask_api.route('/number_of_users')
class GetUsers(Resource):
    def get(self):
        GUD = GetUserDetails(DATA_ROOT_URL)
        return {'number_of_users': GUD.get_total_num_of_users()}


@ flask_api.route('/get_users/<string:distance>')
class GetKeys(Resource):
    def get(self, distance='50'):
        GUD = GetUserDetails(DATA_ROOT_URL)
        return {'users_near_london': GUD.get_all_users_near_city()}
