
class Regal:

    def __init__(self, number, location, products=None, quantity=0):
        if products is None:
            products = []

        self.number = number
        self.location = location
        self.products = products
        self.quantity = quantity

    def take_product(self, product_id):
        for product in self.products:
            if product.name == product_id:
                product.decrementQuantity()
                self.decrement_quantity()

    def decrement_quantity(self):
        self.quantity -= 1
