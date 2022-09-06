# -*- coding: utf-8 -*-
# @Time : 2022/4/3 17:32
# @Author : hhq
# @File : part_BOM.py
import xlrd
xl = xlrd.open_workbook(r"G:\gas_engine\partBOM.xls")
table = xl.sheets()[0]
rows = table.nrows  # 获取一共多少行
cols = table.ncols  # 获取多少列
# todo 获取行值
product_parts = {}  # 成品零件的集合 {成品零件：[[零件,零件数]]}
for i in range(rows):  # 行数遍历
    row_v = table.row_values(i)  # 获取行值
    if i == 0:
        product_parts[row_v[0]] = [[row_v[2], row_v[4]]]
    else:
        if table.row_values(i)[0] == table.row_values(i-1)[0]:  # 前后两件产品相同
            product_parts[row_v[0]].append([row_v[2], row_v[4]])
        else:
            product_parts[row_v[0]] = [[row_v[2], row_v[4]]]
print(product_parts)

