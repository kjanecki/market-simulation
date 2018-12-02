import uuid

class Product:
  def __init__(self, name, kind, price, discount, quantity):
    self.id = uuid.uuid4()
    self.name = name
    self.kind = kind
    self.price = price
    self.discount = discount
    self.quantity = quantity

    def decrementQuantity():
      self.quantity -= 1

    def setValue():
      return {
            'name': setName,
            'kind': setKind,
            'price': setPrice,
            'discount': setDiscount,
            'quantity': setQuantity
           }

    def setName(value):
      self.name = value
    
    def setKind(value):
      self.kind = value
    
    def setPrice(value):
      self.price = value

    def setDiscount(value):
      self.discount = value

    def setQuantity(value):
      self.quantity = value
          