from Market.Shelf import Shelf


class Regal:

    def __init__(self, number, location, size):

        self.number = number
        self.location = location
        self.size = size
        self.product_shelf_map = {}
        self.shelf_list = []
        self.initialize_shelf_list()
        self.next_shelf_index = 0

    def initialize_shelf_list(self):
        index = 0
        direction = 'S'
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if j == self.size[1] - 1:
                    direction = 'N'
                self.shelf_list.append(Shelf(index, (self.location[0]+i, self.location[1]+j), direction=direction))
                index += 1
                print(direction, end=" ")
            print()
        print()

    def add_product(self, product):
        self.product_shelf_map[product.id] = self.next_shelf_index
        self.next_shelf_index += 1
        if self.next_shelf_index > len(self.shelf_list) - 1:
            self.next_shelf_index = 0
