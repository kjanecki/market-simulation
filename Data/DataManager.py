from DataReader import DataReader
from DataWriter import DataWriter

class DataManager:
    def __init__(self):
        self.DataReader = DataReader()
        self.DataWriter = DataWriter()

    @staticmethod
    def read(self):
        self.DataReader.read('./products.xml')

    @staticmethod
    def write(self, data):
        self.DataWriter.write('./result.txt', data)