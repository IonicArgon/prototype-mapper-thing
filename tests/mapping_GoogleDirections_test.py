import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from mapping.GoogleDirections import GoogleDirections

class TestGoogleDirections(unittest.TestCase):
    def setUp(self):
        self.__m_test_name = 'TestGoogleDirections'

        load_dotenv()
        self.__m_api_key = os.getenv("GOOGLE_API_KEY")
        self.__m_route_endpoint = os.getenv("GOOGLE_ROUTE_ENDPOINT")
        self.__m_places_endpoint = os.getenv("GOOGLE_PLACES_ENDPOINT")
        self.__m_google_directions = GoogleDirections(self.__m_api_key, self.__m_route_endpoint, self.__m_places_endpoint)

        self.__m_test_location = "31 Goswell Street, Brampton, ON, Canada"
        self.__m_test_respose = self.__m_google_directions.test_accessor(self.__m_test_location)
    
    def test_ReturnIsNotNone(self):
        self.assertIsNotNone(self.__m_test_respose)
        print(f'[{self.__m_test_name}] Response is not None.')

    def test_ReturnFirstHasPlaceID(self):
        self.assertIsNotNone(self.__m_test_respose[0]["place_id"])
        print(f'[{self.__m_test_name}] Response[0] has place_id of: {self.__m_test_respose[0]["place_id"]}.')

    def test_ReturnFirstDescription(self):
        self.assertTrue(self.__m_test_respose[0]["description"].startswith(self.__m_test_location))
        print(f'[{self.__m_test_name}] Response[0] has description of: {self.__m_test_respose[0]["description"]}.')

if __name__ == '__main__':
    unittest.main()