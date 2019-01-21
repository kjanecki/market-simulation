import xlrd
from random import randint, shuffle

from Market.Product import Product

class ShoppingListGenerator:


    def __init__(self, market):
        self.market = market

    def generate_shopping_lists(self, number=100):
        products = self._get_products()
        shopping_lists = []

        for i in range(1, number):
            shopping_lists.append(self.generate_shopping_list(products))

        return shopping_lists

    def generate_shopping_list(self, products, doCluster=False):
        shopping_list = []
        money_limit = 1000
        number_of_items = randint(5, 30)
        for i in range(0, number_of_items):

            list_item = products[randint(0, len(products)-1)]
            if money_limit - list_item.price - 100 > 0:
                shopping_list.append(list_item)

        if doCluster:
            return self.cluster(shopping_list)
        else:
            return shopping_list

    def _get_list_item(self, products):
        list_item = {'id': 0, 'price': 0}
        product = products[randint(0, len(products)-1)]
        list_item['id'] = product.id
        list_item['price'] = product.price
        list_item
        return list_item

    def _get_products(self):
        book = xlrd.open_workbook(('./examples/products.xlsx'))
        sh = book.sheet_by_index(0)
        col_name = ['name', 'regal', 'price']
        products = []
      
        for i in range(sh.nrows):
            product = Product()

            for j in range(sh.ncols):
                func_map = product.setValue()
                cell_val = sh.cell_value(i, j)
                func_map[col_name[j]](float(cell_val) if col_name[j] != 'name' else cell_val)
            
            products.append(product)

        return products

    def cluster(self, shopping_list):
        buckets = []
        final_shopping_list = []
        for i in range(len(self.market.regals)+1):
            buckets.append([])

        for product in shopping_list:
            buckets[product.departament].append(product)

        shuffle(buckets)

        while len(buckets) != 0:
            final_shopping_list += buckets.pop(0)

        return final_shopping_list
