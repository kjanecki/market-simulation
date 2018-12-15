import xlrd
from Market.Product import Product
from Market.Regal import Regal
from Market.Market import Market

class DataReader:

    def initialize_market(self, path):
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
        col_name = ['name', 'regal', 'price']
        products = []
        regals = []
        
      
        for i in range(1, 10):
            product = Product()
            for j in range(sh.ncols):
                func_map = product.setValue()
                cell_val = sh.cell_value(i, j)
                func_map[col_name[j]](float(cell_val) if col_name[j] != 'name' else cell_val)
            products.append(product)

            added = False
            (lastX, lastY) = (0, 0)
            for regal in regals:
                if(regal.number == product.regal):
                    regal.products.append(product)
                    regal.quantity += product.quantity
                    added = True
                (lastX, lastY) = regal.location
            # TODO: Implement adding new regal position???
            if(added == None):
                regals.append(Regal(product.regal, (lastX + 5, lastY + 4), [product], product.quantity))
        
        return Market(products, regals, None)