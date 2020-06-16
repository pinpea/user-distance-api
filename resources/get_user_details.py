import json
import requests

from resources.calc_distances import calc_haversine_dist_miles, calc_equirectangular_dist_miles
import pandas as pd


class GetUserDetails(object):

    """
    Methods for getting details about user location, both listed and current distance, from a request location. 
    Uses the https://bpdts-test-app.herokuapp.com/ api - see https://bpdts-test-app.herokuapp.com/swagger.json
    """

    def __init__(self, root_url, requested_city='London', find_users_in_range=True, requested_range=50, requested_lat_long=(51.506, -0.1272)):
        self._root_url = root_url

        self._requested_city = requested_city
        
        # set to (lat, long) of London as default
        self._requested_lat_long = requested_lat_long
        self._users = self.get_all_users()

        #If False, only return users who are listed as living in requested city, else also return users in the requested range
        self._find_users_in_range = find_users_in_range 
        
        if requested_range <0:
            requested_range*=1

        self._requested_range = requested_range  # set to 50 miles by default

    def get_all_users(self):
        """ Send query to get all users and return data as a dataframe """
        query_user_url = self._root_url + 'users'
        return pd.DataFrame((requests.get(query_user_url)).json())

    def get_total_num_of_users(self):
        """ return number of rows in dataframe - each row is one user """
        number_of_users = self._users.shape[0]
        return number_of_users

    def get_user_keys(self):
        """
        Lists the available keys available for a user
        """
        available_keys = self._users.columns.values.tolist()
        print(available_keys)
        return available_keys

    def get_users_in_requested_city(self, input_city='London'):
        """
        Returns data frame of users from bpdts-test-app that are listed as living in a given city, London by default.
        """
        query_city_url = self._root_url + 'city/'+input_city+'/users'
        try:
            user_request = requests.get(query_city_url)
            users_in_city = pd.DataFrame(user_request.json())
            user_request.raise_for_status()
            return users_in_city

        except requests.exceptions.HTTPError as err:
            raise NoResultFound(err)

        
    def filter_users_by_distance(self, users,  requested_range=50, requested_lat_long=(51.506, -0.1272)):
        """
        Return users that have are within a requested range of a location. 
        Distance is calculated using the Haversine formula.
        By default, 50 miles from London is used. 
        """
        latitude = pd.to_numeric(users["latitude"])
        longitude = pd.to_numeric(users["longitude"])

        distance = calc_haversine_dist_miles(
            latitude, longitude,   requested_lat_long)
        users['distance_from_city'] = distance

        users_within_range = users.loc[users['distance_from_city']
                                       <= requested_range]
        return users_within_range

    def filter_users_by_distance_equirectangular(self, users, requested_range=50, requested_lat_long=(51.506, -0.1272)):
        """
        Return users that have are within a requested range of a location. 
        Distance is calculated using the equirectangular formula.
        By default, 50 miles from London is used. 
        Quicker than the haversine formula, but reduces in accuracy over long distances.
        """
        latitude = pd.to_numeric(users["latitude"])
        longitude = pd.to_numeric(users["longitude"])

        distance = calc_equirectangular_dist_miles(
            latitude, longitude,   requested_lat_long)

        users['distance_from_city'] = distance
        users_within_range = users.loc[users['distance_from_city']
                                       <= requested_range]
        return users_within_range

    def get_all_users_near_city(self, requested_range=50, city='London', requested_lat_long=(51.506, -0.1272)):
        """
        Returns unique users and their current distance for users who either list themselves as living in the requested city, or whose current coordinates are within a requested range of a city.
        Those who are listed as living in the current city return a distance of 0 from the city.
        """
        users_in_city = self.get_users_in_requested_city()
               
        if self._find_users_in_range == True:
            users_in_range = self.filter_users_by_distance(self._users,
                                                       requested_range, requested_lat_long)
            # merges queries and removes duplicates
            all_users_in_city = (pd.concat(
                [users_in_range, users_in_city]).drop_duplicates(keep=False))
        else:
            # merges queries and removes duplicates
            all_users_in_city = (users_in_city).drop_duplicates(keep=False)
            all_users_in_city['distance_from_city']= np.nan

        # Replace null with 0 for values in calculated distance returned from get_users_in_requested_city()
        all_users_in_city['distance_from_city']= all_users_in_city['distance_from_city'].fillna(value=0) 
        all_users_in_city = all_users_in_city.sort_values('id')

        return all_users_in_city


    # Used for testing
    def call_filter_users_for_test(self): 
        """Public interface to test __filter_users_by_city_test """
        users_in_city = self.__filter_users_by_city_test()
        return users_in_city

    def __filter_users_by_city_test(self,  input_city='London'):
        """
        Return users from bpdts-test-app that are listed as living in the requested city, London by default
        Slow, since calls api multiple times, used in testing to check output.
        """
        number_of_users = int(self.get_total_num_of_users())
        number_relevant_users = 0
        for user_id in range(number_of_users):
            query_user_url = self._root_url + 'user/'+str(user_id+1)
            user = (requests.get(query_user_url)).json()
            if user['city'] == input_city:
                number_relevant_users += 1
        return number_relevant_users

   