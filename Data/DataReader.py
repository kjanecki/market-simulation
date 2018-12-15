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
        
      
        for i in range(sh.nrows):
            product = Product()
            for j in range(sh.ncols):
                product.setValue(col_name[j])(sh.cell_value(rowx=i, colx=j))
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