import xlrd
from Shop.Product import Product

class DataReader:

    def read(self, path):
        colName = ['name', 'kind', 'price', 'discount', 'quantity']
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
      
        for i in range(sh.nrows):
            product = Product()

            for j in range(sh.ncols):
                product.setValue([colName[j]](sh.cell_value(rowx=i, colx=j)))
            
