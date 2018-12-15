class Market:

    def __init__(self, products, regals, cashRegisters):
        self.articles = products
        self.regals = regals
        self.cashRegisters = cashRegisters

    def get_product_position(self, product):
        regal = self.regals[int(product.regal)-1]
        shelf_id = regal.product_shelf_map[product.id]
        shelf = regal.shelf_list[shelf_id]

        i, j = 0, 0
        if shelf.direction == 'S':
            j = -1
        elif shelf.direction == 'N':
            j = 1
        elif shelf.direction == 'E':
            i = -1
        elif shelf.direction == 'W':
            i = 1

        return shelf.location[0] + i, shelf.location[1] + j

