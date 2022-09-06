# -*- coding: utf-8 -*-
# @Time : 2022/4/5 14:21
# @Author : hhq
# @File : machine_number.py
import xlrd

# todo 获取加工机器数量
xl = xlrd.open_workbook(r"G:\gas_engine\machine table.xls")
table = xl.sheets()[0]
rows = table.nrows  # 获取行数
machines = {}
for i in range(1, rows):
    row_ = table.row_values(i)
    machines[row_[1] + row_[4]] = int(row_[5])
# print(machines)
