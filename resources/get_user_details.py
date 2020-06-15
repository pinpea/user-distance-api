import json
import requests

from resources.calc_distances import calc_haversine_dist_miles
import pandas as pd


class GetUserDetails(object):
    """

    """

    def __init__(self, root_url, requested_city='London', requested_range=50, requested_lat_long=(51.506, -0.1272)):
        self._root_url = root_url

        self._requested_city = requested_city
        self._requested_range = requested_range
        self._requested_lat_long = requested_lat_long

        self._users = self.get_all_users() 

    def get_all_users(self):
        query_user_url = self._root_url + 'users'
        return pd.DataFrame((requests.get(query_user_url)).json())

    def get_users_in_requested_city(self, input_city='London'):
        """
        Returns data frame of users from bpdts-test-app that are listed in a given city, London by default.
        """
        query_city_url = self._root_url + 'city/'+input_city+'/users'
        return pd.DataFrame((requests.get(
            query_city_url)).json())

    def get_total_num_of_users(self):
        # return number of rows in DataFrame
        number_of_users = self._users.shape[0]
        return number_of_users

    def get_user_keys(self):
        """
        Lists the available keys available for a user
        """
        available_keys = self._users.columns.values.tolist()
        print(available_keys)
        return {'available_user_keys': json.dumps(available_keys)}

    def filter_users_by_distance(self, requested_range=50):
        """
        Return users that have are within a requested range of a location. 
        Distance is calculated using the Haversine formula.
        By default, 50 miles from London is used. 
        """
        latitude = pd.to_numeric(self._users["latitude"])
        longitude = pd.to_numeric(self._users["longitude"])

        distance = calc_haversine_dist_miles(
            latitude, longitude,   self._requested_lat_long)

        self._users['distance_from_city'] = distance

        users_within_range = self._users.loc[self._users['distance_from_city'] <= 50]

        return users_within_range

    def filter_users_by_city(self,  input_city='London'):
        """
        Return users from bpdts-test-app that list the requested city as their city, London by default
        Slow, since calls api multiple times, used in testing to check output.
        """
        number_of_users = int(self.get_total_num_of_users())
        relevant_users = []
        for user_id in range(number_of_users):
            query_user_url = self._root_url + 'user/'+str(user_id+1)
            user = (requests.get(query_user_url)).json()
            if user['city'] == input_city:
                relevant_users.append(user)
        return relevant_users

    def get_all_users_near_city(self):
        """
        Returns unique users who are either list themselves at the requested city, or whose current coordinates are within a requested range of a city
        """
        users_in_range = self.filter_users_by_distance()
        users_in_city = self.get_users_in_requested_city()

        all_users_in_city = pd.concat(
            [users_in_range, users_in_city]).drop_duplicates(keep=False)  # merges queries and removes duplicates
        all_users_in_city = all_users_in_city.to_json()
        return all_users_in_city
