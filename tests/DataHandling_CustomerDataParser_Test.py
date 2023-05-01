import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from DataHandling.CustomerDataParser import CustomerDataParser

class TestCustomerDataParser(unittest.TestCase):
    def setUp(self):
        self.__m_test_name = 'TestCustomerDataParser'

        load_dotenv()
        self.__m_test_file_path = os.getenv("CUSTOMER_DATA_FILE_PATH")
        self.__m_customer_data_parser = CustomerDataParser(self.__m_test_file_path)

        self.__m_test_location = "38 Battersea Crescent"
        self.__m_test_region = "North York"
        self.__m_test_job_date = [0]

    def test_ReturnIsNotNone(self):
        length = len(list(self.__m_customer_data_parser.get_all_customers()))
        self.assertTrue(length > 0)
        print(f'[{self.__m_test_name}] CustomerDataParser returned {length} customers.')

    def test_ReturnFirstHasAddress(self):
        test_customer = self.__m_customer_data_parser.get_customer(self.__m_test_location)
        self.assertIsNotNone(test_customer['address'])
        self.assertEqual(test_customer['address'], self.__m_test_location)
        print(f'[{self.__m_test_name}] CustomerDataParser returned customer with address: {test_customer["address"]}.')

    def test_ReturnFirstHasRegion(self):
        test_customer = self.__m_customer_data_parser.get_customer(self.__m_test_location)
        self.assertIsNotNone(test_customer['region'])
        self.assertEqual(test_customer['region'], self.__m_test_region)
        print(f'[{self.__m_test_name}] CustomerDataParser returned customer with region: {test_customer["region"]}.')

    def test_ReturnFirstHasWeekdays(self):
        test_customer = self.__m_customer_data_parser.get_customer(self.__m_test_location)
        self.assertIsNotNone(test_customer['weekdays'])
        self.assertEqual(test_customer['weekdays'], self.__m_test_job_date)
        print(f'[{self.__m_test_name}] CustomerDataParser returned customer with weekdays: {test_customer["weekdays"]}.')

    def test_ReturnFirstHasFrequency(self):
        test_customer = self.__m_customer_data_parser.get_customer(self.__m_test_location)
        self.assertIsNotNone(test_customer['frequency'])
        print(f'[{self.__m_test_name}] CustomerDataParser returned customer with frequency: {test_customer["frequency"]}.')

    def test_YieldContainsAll(self):
        counter = 0
        length = len(list(self.__m_customer_data_parser.get_all_customers()))

        for customer in self.__m_customer_data_parser.get_all_customers():
            self.assertIsNotNone(customer['address'])
            self.assertIsNotNone(customer['region'])
            self.assertIsNotNone(customer['weekdays'])
            self.assertIsNotNone(customer['frequency'])
            print(f'[{self.__m_test_name}] CustomerDataParser yielded customer: {customer["address"]}\n\twith region: {customer["region"]}\n\tand weekdays: {customer["weekdays"]}\n\tand frequency: {customer["frequency"]}.')
            counter += 1

        self.assertEqual(counter, length)

if __name__ == '__main__':
    unittest.main()
