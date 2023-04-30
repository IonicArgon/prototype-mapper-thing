import csv
import datetime
import calendar

class ContractorDataParser():
    def __init__(self, p_file_path):
        self.__m_file_path = p_file_path
        self.__m_contractor_data = {}

        self.__parse()

    def __parse(self):
        with open(self.__m_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip header row
            for row in csv_reader:
                ##todo: also figure out what i want to use for the dictionary keys

                entry = {}
                entry['name'] = row[0]
                entry['address'] = row[1]
                entry['regions'] = row[2].split(';')
                entry['available'] = [self.__weekday_to_int(date) for date in row[3].split(';')]

                self.__m_contractor_data[row[0]] = entry

    ##todo: is this the most pythonic way to do this?
    def __weekday_to_int(self, p_weekday):
        REFERENCE_LIST = [day.upper() for day in list(calendar.day_name)]
        return REFERENCE_LIST.index(p_weekday.upper())

    def get_contractor(self, p_name):
        return self.__m_contractor_data[p_name]
    
    def get_all_contractors(self):
        'NOTE: THIS IS A GENERATOR, DON\'T BE DUMB'
        for contractor in self.__m_contractor_data:
            yield self.__m_contractor_data[contractor]
