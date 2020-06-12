import json
import requests
from flask import Flask
from flask_restx import Api, Resource

flask_app = Flask(__name__)
flask_api = Api(flask_app)

import resources.routes







