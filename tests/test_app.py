
import pytest
# import unittest
import requests
import json
import time
from resources.get_user_details import GetUserDetails

url = 'http://127.0.0.1:5000/'  # default flask app url
DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'


def test_response():
    response = requests.get(url)
    assert response.status_code == 200


def test_app_output():
    response = requests.get(url + '/information')
    expected_output = {'api_overview': 'todo'}
    assert expected_output == response.json()


def test_number_of_users():
    expected_total_users = 1000
    response = requests.get(url + '/number_of_users')
    response_as_dict = response.json()
    num_of_users_returned = response_as_dict['number_of_users']
    assert int(num_of_users_returned) == expected_total_users


#!-- Unit tests of GUD --

# Uncomment to run the following test - very slow, used for testing only

# def test_cityquery_and_userlist():
#     """Compare the outputs for the city/City/users query with the output of users in cities when filtering by city i.e., the city field for /user/id query. Very slow, since sending a query per user, used for testing only. """
#     print("\n Querying all users, please wait... \n")
#     GUD = GetUserDetails(DATA_ROOT_URL)
#     num_users_filter_by_city = GUD.filter_users_by_city()
#     num_listed_users_in_city = GUD.get_users_in_requested_city().shape[0]
#     assert num_users_filter_by_city == num_listed_users_in_city


def test_compare_calc_methods():
    GUD = GetUserDetails(DATA_ROOT_URL)
    tic = time.perf_counter()
    user_distances_haversine = GUD.filter_users_by_distance(GUD._users)
    toc = time.perf_counter()
    tictoc1 = toc - tic

    tic = time.perf_counter()
    user_distances_equirectangular = GUD. filter_users_by_distance_equirectangular(
        GUD._users)
    toc = time.perf_counter()

    tictoc2 = toc - tic

    print(f"Haversine was {tictoc1:0.4f} seconds\n")
    print(f"Equirectangular was {tictoc2:0.4f} seconds\n")

    assert user_distances_haversine.shape[0] == user_distances_equirectangular.shape[0]
