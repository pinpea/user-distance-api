import pytest
import requests
import json

url = 'http://127.0.0.1:5000/' #default flask app url

def test_hello_world():
   response = requests.get(url) 
   assert response.status_code == 200

def test_app_output():
   response = requests.get(url+'hello') 
   expected_output = {'hello': 'world'}
   assert expected_output == response.json()
   