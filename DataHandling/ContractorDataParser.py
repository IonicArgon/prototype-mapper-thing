import csv
import calendar

class ContractorDataParser():
    def __init__(self, p_file_path=None):
        self.__m_file_path = p_file_path
        self.__m_contractor_data = None

        if p_file_path != None:
            self.__parse()

    def __parse(self):
        self.__m_contractor_data = {}
        with open(self.__m_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            ##todo: make a check to see if the header row is in the correct format

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
    
    def set_file_path(self, p_file_path):
        if ".csv" in p_file_path:
            self.__m_file_path = p_file_path
            self.__parse()
            return 0
        else:
            return -1

    def get_contractor(self, p_name):
        if self.__m_contractor_data != None:
            return self.__m_contractor_data[p_name]
        else:
            return -1
    
    def get_all_contractors(self):
        'NOTE: THIS IS A GENERATOR, DON\'T BE DUMB'
        if self.__m_contractor_data != None:
            for contractor in self.__m_contractor_data:
                yield self.__m_contractor_data[contractor]
        else:
            yield -1
