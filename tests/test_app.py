
import pytest
# import unittest
import requests
import json

url = 'http://127.0.0.1:5000/'  # default flask app url


def test_hello_world():
    response = requests.get(url)
    assert response.status_code == 200


def test_app_output():
    response = requests.get(url + 'hello')
    expected_output = {'hello': 'world'}
    assert expected_output == response.json()


def test_number_of_users():
    expected_total_users = 1000
    response = requests.get(url + '/number_of_users')
    response_as_dict = response.json()
    num_of_users_returned = response_as_dict['number_of_users']
    assert int(num_of_users_returned) == expected_total_users
