class Regal:

    def __init__(self, number, location, products=None):
        if products is None:
            products = []

        self.number = number
        self.location = location
        self.products = products