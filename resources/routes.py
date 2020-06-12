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


@flask_api.route('/number_of_users')
class GetUsers(Resource):
    def get(self):
        GUD = GetUserDetails(DATA_ROOT_URL)
        return GUD.get_number_of_users()
