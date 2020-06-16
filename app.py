import json
import requests
from flask import Flask
from flask_restx import Api, Resource

flask_app = Flask(__name__)
flask_api = Api(flask_app, version='1.0', title='User Distance API',
                description='API to search for users listed in a city, or within a given distance from a city - 50 miles from London by default')

api_namespace = flask_api.namespace("user_distances", "requests to get number of users near, or living in a city")


import resources.routes






