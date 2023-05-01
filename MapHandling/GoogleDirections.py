import requests
import urllib.parse

## so as it currently stands, the Google Maps Embed API does not support waypoint optimization
## the solution for now (because i don't want to switch to JS) is to use the Directions API to get the optimized route
## and then use the waypoint order to display the Embed API map with the optimized route
##NOTE: this costs extra money in the long run, it's more ideal if we made the project in JS to begin with but i already started w/ python b/c i'm more familiar with it

class GoogleDirections:
    def __init__(self, p_api_key, p_directions_endpoint):
        self.__m_api_key = p_api_key
        self.__m_directions_endpoint = p_directions_endpoint
        self.__m_stored_directions = None

    def __get_directions(self, p_origin, p_destination, p_waypoints: list):
        payload = {}
        headers = {}

        url_origin = '?origin=place_id:' + urllib.parse.quote_plus(p_origin)
        url_destination = '&destination=place_id:' + urllib.parse.quote_plus(p_destination)
        waypoints = "|".join(["place_id:" + waypoint for waypoint in p_waypoints])
        url_waypoints = '&waypoints=optimize:true|' + urllib.parse.quote_plus(waypoints)
        url_key = '&key=' + self.__m_api_key

        url = self.__m_directions_endpoint + url_origin + url_destination + url_waypoints + url_key
        print(url)

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            self.__m_stored_directions = response.json()
        else:
            self.__m_stored_directions = None
    
    def get_optimized_waypoints(self, p_origin, p_destination, p_waypoints: list):
        self.__get_directions(p_origin, p_destination, p_waypoints)
        if self.__m_stored_directions is not None:
            return self.__m_stored_directions["routes"][0]["waypoint_order"]
        else:
            return None
