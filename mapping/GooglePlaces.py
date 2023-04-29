# space for imports as i see fit
import requests
import urllib.parse

class GooglePlaces:
    def __init__(self, p_api_key, p_places_endpoint):
        self.__m_api_key = p_api_key
        self.__m_places_endpoint = p_places_endpoint

    def __get_place(self, p_place_name):
        payload = {}
        headers = {}

        url_input = '?input=' + urllib.parse.quote_plus(p_place_name)
        url_type = '&types=geocode'
        url_key = '&key=' + self.__m_api_key

        url = self.__m_places_endpoint + url_input + url_type + url_key

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()["predictions"]
        else:
            return None
        
    def test_accessor(self, p_place_name):
        return self.__get_place(p_place_name)