# -*- coding: utf-8 -*-
# @Time : 2022/4/5 14:47
# @Author : hhq
# @File : product_num.py
import xlrd
# todo 获取每种零件产品的数量
xl = xlrd.open_workbook(r"G:\gas_engine\product_num.xls")
table = xl.sheets()[0]
rows = table.nrows
products = {}
for i in range(1, rows):
    row_ = table.row_values(i)
    if row_[0] not in products:
        products[row_[0]] = int(row_[1])
    else:
        products[row_[0]] += int(row_[1])
print(products)