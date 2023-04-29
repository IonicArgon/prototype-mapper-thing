import csv
import datetime

class CustomerDataParser():
    def __init__(self, p_file_path):
        self.__m_file_path = p_file_path
        self.__m_customer_data = {}

        self.__parse()

    def __parse(self):
        with open(self.__m_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip header row
            for row in csv_reader:
                ##todo: figure out what i want to use for the dictionary keys
                ##todo: i figure i'll just hash a customer id or smth
                ##todo: for now just use the address

                entry = {}
                entry['address'] = row[0]
                entry['region'] = row[1]
                entry['job date'] = datetime.datetime.strptime(row[2], '%Y/%m/%d')

                self.__m_customer_data[row[0]] = entry

    def get_customer(self, p_address):
        return self.__m_customer_data[p_address]
    
    def get_all_customers(self):
        'NOTE: THIS IS A GENERATOR, DON\'T BE DUMB'
        for customer in self.__m_customer_data:
            yield self.__m_customer_data[customer]
