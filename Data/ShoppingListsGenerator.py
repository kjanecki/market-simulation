import xlrd
from random import randint
from Market.Product import Product

class ShoppingListGenerator:
    def generate_shopping_lists(self, number=100):
        products = self._get_products()
        shopping_lists = []

        for i in range(1, number):
            shopping_lists.append(self.generate_shopping_list(products))

        return shopping_lists

    def generate_shopping_list(self, products):
        shopping_list = []
        money_limit = 1000
        number_of_items = randint(2, len(products)-1)
        for i in range(0, number_of_items):

            list_item = products[randint(0, len(products)-1)]
            if money_limit - list_item.price - 100 > 0:
                shopping_list.append(list_item)
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