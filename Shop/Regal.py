class Regal:
  def __init__(self, number, products, quantity):
    self.number = number
    self.products = products
    self.quantity = quantity

    def takeProduct(self, productId):
        for product in self.products:
            if product.name == productId:
                product.decrementQuantity()
                self.decrementQuantity()

    def decrementQuantity():
        self.quantity -= 1

