import requests
import urllib.parse
import time

class GoogleDistanceMatrix:
    def __init__(self, p_api_key, p_matrix_endpoint):
        self.__m_api_key = p_api_key
        self.__m_matrix_endpoint = p_matrix_endpoint
        self.__m_stored_matrix = None

    def __get_matrix(self, p_origins: list, p_destinations: list):
        payload = {}
        headers = {}

        origins = "|".join(["place_id:" + origin for origin in p_origins])
        url_origins = '?origins=' + urllib.parse.quote_plus(origins)
        destinations = "|".join(["place_id:" + destination for destination in p_destinations])
        url_destinations = '&destinations=' + urllib.parse.quote_plus(destinations)
        url_mode = '&mode=driving'
        url_key = '&key=' + self.__m_api_key

        url = self.__m_matrix_endpoint + url_origins + url_destinations + url_mode + url_key

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            self.__m_stored_matrix = []
            for matrix_row in response.json()["rows"]:
                row = []
                for matrix_element in matrix_row["elements"]:
                    cell = []
                    cell.append(matrix_element["distance"]["value"])
                    cell.append(matrix_element["duration"]["value"])
                    row.append(cell)
                self.__m_stored_matrix.append(row)
        else:
            self.__m_stored_matrix = None

    def calculate_matrix(self, p_origins: list, p_destinations: list):
        self.__get_matrix(p_origins, p_destinations)
        if self.__m_stored_matrix is not None:
            return 0
        else:
            return -1
        
    def get_matrix(self):
        return self.__m_stored_matrix
    
    def get_matrix_row(self, p_row):
        return self.__m_stored_matrix[p_row]
    
    def get_matrix_cell(self, p_row, p_col):
        return self.__m_stored_matrix[p_row][p_col]
    
    def get_closest_distance_row(self, p_row):
        closest = None
        for col in self.get_matrix_row(p_row):
            if closest is None:
                closest = col
            elif col[0] < closest[0]:
                closest = col

        return closest
    
    def get_furthest_distance_row(self, p_row):
        furthest = None
        for col in self.get_matrix_row(p_row):
            if furthest is None:
                furthest = col
            elif col[0] > furthest[0]:
                furthest = col

        return furthest


