# -*- coding: utf-8 -*-
# @Time : 2022/4/4 21:18
# @Author : hhq
# @File : assembly_process.py
import xlrd
xl = xlrd.open_workbook(r"G:\gas_engine\assembly_process.xls")  # 获得数据位置
table = xl.sheets()[0]
rows = table.nrows
cols = table.ncols
# todo 获取行值
assemblys = {}  # 装配件
for i in range(1, rows):
    row_v = table.row_values(i)
    if i == 0 and row_v[9] != '':  # 此处避免读入空值
        assemblys[(row_v[0], row_v[4]+row_v[3], float(row_v[5]))] = [(row_v[9], int(row_v[11]))]
        machine_area, time = row_v[4]+row_v[3], float(row_v[5])
    else:
        if table.row_values(i)[0] == table.row_values(i-1)[0] and row_v[9] != '':  # 是同一装配件
            machine_area_, time_ = machine_area, time
            assemblys[(row_v[0], machine_area, time)].append((row_v[9], int(row_v[11])))
        else:
            if row_v[9] != '':
                assemblys[(row_v[0], row_v[4]+row_v[3], float(row_v[5]))] = [(row_v[9], int(row_v[11]))]
                machine_area, time = row_v[4]+row_v[3], float(row_v[5])
# print(assemblys)
