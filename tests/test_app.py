
import pytest
import requests
import json
import time
from resources.get_user_details import GetUserDetails
from app import api_namespace

name_space = api_namespace.name
url = 'http://127.0.0.1:5000/'+name_space # default flask app url

DATA_ROOT_URL = 'https://bpdts-test-app.herokuapp.com/'


def test_response():
    response = requests.get(url + '/information')
    assert response.status_code == 200


def test_app_output():
    response = requests.get(url + '/information')
    expected_output = {'api_overview': 'todo'}
    assert expected_output == response.json()


def test_total_number_of_users():
    expected_total_users = 1000
    response = requests.get(url + '/get_total_number_of_users')
    response_as_dict = response.json()
    num_of_users_returned = response_as_dict['total_number_of_users']
    assert int(num_of_users_returned) == expected_total_users

def test_users_in_50miles():
    """ Validate that the London specific and the general method give the same output """
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city=London&return_users=false&find_users_in_range=true&distance=50&latitude=51.506&longitude=-0.1272')).json()
    response_london_specific = (requests.get(url + '/get_number_of_users_in_range')).json()

    assert response_general['number_of_users'] == response_london_specific['number_of_users']

def test_junk_input_response():
    """ If parameters set incorrectly the request is set to request with default parameters"""
    response_general = (requests.get(url + '/get_number_of_users_in_range/?junk')).json()
    response_london_specific = (requests.get(url + '/get_number_of_users_in_range')).json()

    assert response_general['number_of_users'] == response_london_specific['number_of_users']


# def test_error_handling():
#     response_general = (requests.get(url + '/get_number_of_users_in_range/?kity=London&return_users=false&find_users_in_range=true&distance=50&latitude=51.506&longitude=-0.1272')).json()
def test_returned_keys():
    """ Check for errors in the returned keys when users are not returned"""
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Dhangarhi'
    test_find_users_in_range = 'false'
    test_return_users = 'false'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    
    expected_keys = ['number_of_users']
    assert expected_keys == list(response_general.keys())


def test_returned_keys_users():
    """ Check for errors in the returned keys when users are returned"""
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Dhangarhi'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    
    expected_keys = ['number_of_users', 'users' ]
    assert expected_keys == list(response_general.keys())

def test_users_for_returned_city():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Dhangarhi'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()
    response_from_gud = GUD.get_users_in_requested_city(test_city)

    for i, v in enumerate (response_from_gud['id'].values):
        if response_general['users'][i]['id'] != v :
            assert False
    assert True


def test_returned_cities():
    GUD = GetUserDetails(DATA_ROOT_URL)    
    test_city = 'Dhangarhi'
    test_find_users_in_range = 'false'
    test_return_users = 'true'
    
    response_general = (requests.get(url + '/get_number_of_users_in_range/?city='+test_city+'&return_users='+test_return_users+'&find_users_in_range='+test_find_users_in_range)).json()

    for user in response_general['users']:
        test_user_response = (requests.get(DATA_ROOT_URL + '/user/'+ str(user['id']))).json()

        if test_user_response['city'] != test_city :
            assert False
            return
    assert True

    
#!-- Validation of output of GUD methods--

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

    print(f"\nHaversine was calculated in {tictoc1:0.4f} seconds\n")
    print(f"Equirectangular was calculated in {tictoc2:0.4f} seconds\n")

    assert user_distances_haversine.shape[0] == user_distances_equirectangular.shape[0]



# Uncomment to run the following test - very slow, used for testing only

# def test_cityquery_and_userlist():
#     """Compare the outputs for the city/City/users query with the output of users in cities when filtering by city i.e., the city field for /user/id query. Very slow, since sending a query per user, used for testing only. """
#     print("\n Querying all users, please wait... \n")
#     GUD = GetUserDetails(DATA_ROOT_URL)
#     num_users_filter_by_city = GUD.call_filter_users_for_test()
#     num_listed_users_in_city = GUD.get_users_in_requested_city().shape[0]
#     assert num_users_filter_by_city == num_listed_users_in_city

