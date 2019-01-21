import xlrd
from Market.Product import Product
from Market.Regal import Regal
from Market.Market import Market


class DataReader:

    def initialize_market(self, path, products_number=200, regals_number=14, regal_size=(15, 5)):
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
        col_name = ['name', 'regal', 'price']
        products = []
        regals = self.initialize_regal_list(regals_number, regal_size)

        for i in range(1, products_number):
            product = Product()
            for j in range(sh.ncols):
                func_map = product.setValue()
                cell_val = sh.cell_value(i, j)
                func_map[col_name[j]](float(cell_val) if col_name[j] != 'name' else cell_val)

            added = False
            for regal in regals:
                if regal.number == product.regal:
                    product.setDepartament(regal.number)
                    regal.add_product(product)
                    added = True

            if added:
                products.append(product)

        checkouts = []
        for i in range(4, 48, 3):
            checkouts.append((50 - 1, i))

        return Market(products, regals, checkouts)

    def initialize_regal_list(self, regals_number, regal_size):
        regals = []
        locations = [(5, 8), (5, 14), (5, 20), (5, 26), (5, 32), (5, 38), (5, 44),
                     (30, 8), (30, 14), (30, 20), (30, 26), (30, 32), (30, 38), (30, 44)]

        for i in range(regals_number):
            print(i)
            regals.append(Regal(i+1, locations[i], regal_size))

        regals.append(Regal(len(regals)+1, (5, 7), (15, 0), type="single", direction="S"))
        regals.append(Regal(len(regals)+1, (30, 7), (15, 0), type="single", direction="S"))

        return regals

1