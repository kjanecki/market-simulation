import xlrd
from random import randint
from Market.Product import Product

class ShoppingListGenerator:
    def generate_shopping_lists(self):
        products = self._get_products()
        shopping_lists = []

        for i in range(1, 50):
            shopping_lists.append(self._generate_shopping_list(products))

        return shopping_lists


    def _generate_shopping_list(self, products):
        shopping_list = []
        money_limit = 1000
        number_of_items = randint(2, len(products)-1)
        for i in range(0, number_of_items):
            list_item = self._get_list_item(products)
            if(money_limit - list_item['price'] > 0):
                shopping_list.append(list_item)
        return shopping_list

    def _get_list_item(self, products):
        list_item = {'id': -1, 'price': 0}
        product = products[randint(0, len(products)-1)]
        list_item['id'] = product.id
        list_item['price'] = product.price
        return list_item

    def _get_products(self):
        book = xlrd.open_workbook(('./examples/products.xlsx'))
        sh = book.sheet_by_index(0)
        col_name = ['name', 'regal', 'price']
        products = []
      
        for i in range(sh.nrows):
            product = Product()

            for j in range(sh.ncols):
                product.setValue(col_name[j])(sh.cell_value(rowx=i, colx=j))
            
            products.append(product)

        return products