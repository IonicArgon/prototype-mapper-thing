import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from DataHandling.ContractorDataParser import ContractorDataParser

class TestContractorDataParser(unittest.TestCase):
    def setUp(self):
        self.__m_test_name = 'TestContractorDataParser'

        load_dotenv()
        self.__m_test_file_path = os.getenv("CONTRACTOR_DATA_FILE_PATH")
        self.__m_contractor_data_parser = ContractorDataParser(self.__m_test_file_path)

        self.__m_test_name = "Bob Smith"
        self.__m_test_address = "21 Fennimore Crescent"
        self.__m_test_regions = ["North York", "Toronto"]
        self.__m_test_available = [0, 2]

    def test_ReturnIsNotNone(self):
        length = len(list(self.__m_contractor_data_parser.get_all_contractors()))
        self.assertTrue(length > 0)
        print(f'[{self.__m_test_name}] ContractorDataParser returned {length} contractors.')

    def test_ReturnFirstHasName(self):
        test_contractor = self.__m_contractor_data_parser.get_contractor(self.__m_test_name)
        self.assertIsNotNone(test_contractor['name'])
        self.assertEqual(test_contractor['name'], self.__m_test_name)
        print(f'[{self.__m_test_name}] ContractorDataParser returned contractor with name: {test_contractor["name"]}.')

    def test_ReturnFirstHasAddress(self):
        test_contractor = self.__m_contractor_data_parser.get_contractor(self.__m_test_name)
        self.assertIsNotNone(test_contractor['address'])
        self.assertEqual(test_contractor['address'], self.__m_test_address)
        print(f'[{self.__m_test_name}] ContractorDataParser returned contractor with address: {test_contractor["address"]}.')

    def test_ReturnFirstHasRegions(self):
        test_contractor = self.__m_contractor_data_parser.get_contractor(self.__m_test_name)
        self.assertIsNotNone(test_contractor['regions'])
        self.assertListEqual(test_contractor['regions'], self.__m_test_regions)
        print(f'[{self.__m_test_name}] ContractorDataParser returned contractor with regions: {test_contractor["regions"]}.')

    def test_ReturnFirstHasAvailable(self):
        test_contractor = self.__m_contractor_data_parser.get_contractor(self.__m_test_name)
        self.assertIsNotNone(test_contractor['available'])
        self.assertListEqual(test_contractor['available'], self.__m_test_available)
        print(f'[{self.__m_test_name}] ContractorDataParser returned contractor with available: {test_contractor["available"]}.')

    def test_YieldContainsAll(self):
        counter = 0
        length = len(list(self.__m_contractor_data_parser.get_all_contractors()))

        for contractor in self.__m_contractor_data_parser.get_all_contractors():
            self.assertIsNotNone(contractor['name'])
            self.assertIsNotNone(contractor['address'])
            self.assertIsNotNone(contractor['regions'])
            self.assertIsNotNone(contractor['available'])
            print(f'[{self.__m_test_name}] ContractorDataParser yielded contractor: {contractor["name"]}\n\twith address: {contractor["address"]}\n\tand regions: {contractor["regions"]}\n\tand available: {contractor["available"]}.')
            counter += 1

        self.assertEqual(counter, length)

if __name__ == '__main__':
    unittest.main()