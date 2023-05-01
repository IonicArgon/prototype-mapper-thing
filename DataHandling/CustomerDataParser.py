import csv
import calendar

class CustomerDataParser():
    def __init__(self, p_file_path=None):
        self.__m_file_path = p_file_path
        self.__m_customer_data = None

        if p_file_path != None:
            self.__parse()

    def __parse(self):
        self.__m_customer_data = {}

        with open(self.__m_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            ##todo: make a check to see if the header row is in the correct format

            next(csv_reader) # skip header row
            for row in csv_reader:
                ##todo: figure out what i want to use for the dictionary keys
                ##todo: i figure i'll just hash a customer id or smth
                ##todo: for now just use the address

                entry = {}
                entry['address'] = row[0]
                entry['region'] = row[1]
                entry['weekdays'] = [self.__weekday_to_int(date) for date in row[2].split(';')]
                entry['frequency'] = row[3]

                self.__m_customer_data[row[0]] = entry

    def __weekday_to_int(self, p_weekday):
        REFERENCE_LIST = [day.upper() for day in list(calendar.day_name)]
        return REFERENCE_LIST.index(p_weekday.upper())

    def set_file_path(self, p_file_path):
        if ".csv" in p_file_path:
            self.__m_file_path = p_file_path
            self.__parse()
            return 0
        else:
            return -1

    def get_customer(self, p_address):
        if self.__m_customer_data != None:
            return self.__m_customer_data[p_address]
        else:
            return -1
    
    def get_all_customers(self):
        'NOTE: THIS IS A GENERATOR, DON\'T BE DUMB'
        if self.__m_customer_data != None:
            for customer in self.__m_customer_data:
                yield self.__m_customer_data[customer]
        else:
            yield -1
