import json
import requests


class GetUserDetails(object):
    def __init__(self, root_url):
        self._root_url = root_url
        self._query_user_url = root_url + 'users'

    def get_number_of_users(self):
        response = requests.get(self._query_user_url)
        number_of_users = str(len(response.json()))
        return {'number_of_users': number_of_users}
