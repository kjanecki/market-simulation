import json
class DataWriter:
    
    def save_results(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)