from DataReader import DataReader
from DataWriter import DataWriter

class DataManger: 
    @staticmethod
    def initialize_market():
        return DataReader().initialize_market(('./examples/products.xlsx'))

    @staticmethod
    def save_results(results):
        DataWriter().save_results('./examples/result.txt', results)