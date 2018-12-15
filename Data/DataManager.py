from Data.DataReader import DataReader
from Data.DataWriter import DataWriter

class DataManager:
    @staticmethod
    def initialize_market():
        return DataReader().initialize_market('Data/examples/products.xlsx')

    @staticmethod
    def save_results(results):
        DataWriter().save_results('Data/examples/result.txt', results)