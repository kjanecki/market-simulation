import uuid
class ShoppingList:

    def _init_(self, shoppingItems):
        self.id = uuid.uuid4()
        self.shoppingItems = shoppingItems

    def crossoutItem(self, productId):
        for index, item in enumerate(self.shoppingItems):
            if item.productId == productId:
                self.shoppingItems.pop(index)
