import json
class DataWriter:
    
    def write(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)