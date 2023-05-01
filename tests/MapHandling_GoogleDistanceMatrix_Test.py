import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from MapHandling.GoogleDistanceMatrix import GoogleDistanceMatrix
from MapHandling.GooglePlaces import GooglePlaces
from DataHandling.CustomerDataParser import CustomerDataParser

class TestGoogleDistanceMatrix(unittest.TestCase):
    def setUp(self):
        self.__m_test_name = 'TestGoogleDistanceMatrix'

        load_dotenv()
        self.__m_api_key = os.getenv("GOOGLE_API_KEY")
        self.__m_distance_matrix_endpoint = os.getenv("GOOGLE_DISTANCE_MATRIX_ENDPOINT")
        self.__m_places_endpoint = os.getenv("GOOGLE_PLACES_ENDPOINT")
        self.__m_google_distance_matrix = GoogleDistanceMatrix(self.__m_api_key, self.__m_distance_matrix_endpoint)
        self.__m_google_places = GooglePlaces(self.__m_api_key, self.__m_places_endpoint)

        self.__m_test_customer_path = os.getenv("CUSTOMER_DATA_FILE_PATH")
        self.__m_test_customer_data_parser = CustomerDataParser(self.__m_test_customer_path)

        self.__m_test_origin = "21 Fennimore Crescent, North York"
        self.__m_test_origin = [self.__m_google_places.get_place_id(self.__m_test_origin)]

        self.__m_test_destinations = []
        for customer in self.__m_test_customer_data_parser.get_all_customers():
            self.__m_test_destinations.append(self.__m_google_places.get_place_id(customer['address']))

        self.__m_google_distance_matrix.calculate_matrix(self.__m_test_origin, self.__m_test_destinations)

    def test_ReturnIsNotNone(self):
        matrix = self.__m_google_distance_matrix.get_matrix()
        self.assertIsNotNone(matrix)
        print(f'[{self.__m_test_name}] Response is not None.')
        for i in range(len(matrix)):
            print(f'[{self.__m_test_name}] Row {i}: {matrix[i]}')

    def test_ReturnRowIsNotNone(self):
        row = self.__m_google_distance_matrix.get_matrix_row(0)
        self.assertIsNotNone(row)
        print(f'[{self.__m_test_name}] Row 0 is not None.')
        print(f'[{self.__m_test_name}] Row 0: {row}')

    def test_ReturnCellIsNotNone(self):
        cell = self.__m_google_distance_matrix.get_matrix_cell(0, 0)
        self.assertIsNotNone(cell)
        print(f'[{self.__m_test_name}] Cell 0, 0 is not None.')
        print(f'[{self.__m_test_name}] Cell 0, 0: {cell}')

if __name__ == '__main__':
    unittest.main()



