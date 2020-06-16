import json
import requests
from flask import Flask
from flask_restx import Api, Resource

flask_app = Flask(__name__)
flask_api = Api(flask_app, version='1.0', title='User Distance API',
                description='API that calls the bpdts-test-app API and returns users listed in a city and, optionally, within a given distance from a city - 50 miles from London by default')

api_namespace = flask_api.namespace("user_distances")


import resources.routes






