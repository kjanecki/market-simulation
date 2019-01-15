import uuid

class Product:
    def __init__(self, name='', regal=0, price=0):
        self.id = uuid.uuid4()
        self.name = name
        self.regal = regal
        self.price = price

    def setValue(self):
        return {
            'name': self.setName,
            'regal': self.setRegal,
            'price': self.setPrice
        }

    def setName(self, value):
        self.name = value

    def setRegal(self, value):
        self.regal = value

    def setPrice(self, value):
        self.price = value
