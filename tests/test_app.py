import pytest
import requests

url = 'http://127.0.0.1:5000/' #default flask app url

def test_hello_world():
   resp = requests.get(url) 
   assert resp.status_code == 200