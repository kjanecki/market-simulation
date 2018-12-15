import uuid

class Product:
    def __init__(self, name='', regal=0, price=0):
        self.id = uuid.uuid4()
        self.name = name
        self.regal = regal
        self.price = price

        def setValue():
            return {
                'name': setName,
                'regal': setRegal,
                'price': setPrice
            }

        def setName(value):
            self.name = value

        def setRegal(value):
            self.regal = value

        def setPrice(value):
            self.price = value