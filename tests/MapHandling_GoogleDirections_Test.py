import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from MapHandling.GoogleDirections import GoogleDirections
from MapHandling.GooglePlaces import GooglePlaces
from DataHandling.CustomerDataParser import CustomerDataParser


class TestGoogleDirections(unittest.TestCase):
    def setUp(self):
        self.__m_test_name = 'TestGoogleDirections'

        load_dotenv()
        self.__m_api_key = os.getenv("GOOGLE_API_KEY")
        self.__m_directions_endpoint = os.getenv("GOOGLE_DIRECTIONS_ENDPOINT")
        self.__m_places_endpoint = os.getenv("GOOGLE_PLACES_ENDPOINT")
        self.__m_google_directions = GoogleDirections(self.__m_api_key, self.__m_directions_endpoint)
        self.__m_google_places = GooglePlaces(self.__m_api_key, self.__m_places_endpoint)

        self.__m_test_file_path = os.getenv("CUSTOMER_DATA_FILE_PATH")
        self.__m_test_customer_data_parser = CustomerDataParser(self.__m_test_file_path)

        self.__m_test_origin = "21 Fennimore Crescent, North York"
        self.__m_test_origin = self.__m_google_places.get_place_id(self.__m_test_origin)
        self.__m_test_destination = "61 Houston Crescent, North York"
        self.__m_test_destination = self.__m_google_places.get_place_id(self.__m_test_destination)

        self.__m_test_waypoints = []
        for customer in self.__m_test_customer_data_parser.get_all_customers():
            self.__m_test_waypoints.append(self.__m_google_places.get_place_id(customer['address']))

        self.__m_test_respose = self.__m_google_directions.get_optimized_waypoints(self.__m_test_origin, self.__m_test_destination, self.__m_test_waypoints)

    def test_ReturnIsNotNone(self):
        self.assertIsNotNone(self.__m_test_respose)
        print(f'[{self.__m_test_name}] Response is not None.')
        print(f'[{self.__m_test_name}] Optimized waypoint order is: {self.__m_test_respose}.')

if __name__ == '__main__':
    unittest.main()
