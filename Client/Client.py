class Client:
    
    def __init__(self, shoppingList, budget):
        self.shoppingList = shoppingList
        self.budget = budget

    def decreaseBudget(self, value):
        self.budget -= value

    def crossoutItemFromList(self, productId):
        self.shoppingList.crossoutItem(productId)