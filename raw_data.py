# -*- coding: utf-8 -*-
# @Time : 2022/4/1 9:14
# @Author : hhq
# @File : raw_data.py
# todo 对excel操作
import xlrd
xl = xlrd.open_workbook(r"G:\gas_engine\raw_job_process.xls")
table = xl.sheets()[0]
# row_name = table.row_values(0)  # 获取第一行内容
# col = table.col_values(0)  # 获取第一列内容
# print(table.col_values(0, 0, 4))  # 获取第0~4行（不含第四行）
# data = table.cell(2, 0).value  # 获取第几行第几个（从0开始）
rows = table.nrows  # 获取一共多少行
cols = table.ncols  # 获取多少列
no_before = []  # 获取加工前编号
no_after = []  # 获取加工后编号
ope_num = []  # 获取各组件工序数量
values = []  # 加工名称和加工时间合集
for i in range(1, rows):
    row_ = table.row_values(i)  # 获取行值
    if row_[5] != '' and row_[6] != '':  # 工序名和工序时间均不为空
        values.append([int(row_[3]), row_[5], float(row_[6]), row_[8]+row_[7]])  # 所有工序列表
    if row_[0] != '':  # 零件不为空
        no_before.append(row_[0])  # 序号集合-零件任务集合
        no_after.append(row_[1])  # 加工后集合
        ope_num.append(row_[4])  # 工序数量
for n in range(len(ope_num)):  # 对工序数遍历
    v = int(ope_num[n])  # 将字符转化为数字
    ope_num[n] = v
'''l = [x[0] for x in values]  # l为values中第一列，缺失数据特征是其与相邻数字之差不为1
head_tail = []  # 首位序号不满足均值算法
for k in range(len(l)):
    if 0<k<len(l)-1:
        a = l[k-1]
        b = l[k+1]
        if l[k] != (a+b) / 2:
            head_tail.append(k)
# head_tail为特殊索引工序序号
c = []  # 理论上head_tail全部为相差为1的两个数字序号索引间断组成。不满足的索引为特殊索引
for bb in range(len(head_tail)):
    if 0<bb<len(head_tail)-1:
        if abs(head_tail[bb]-head_tail[bb-1]) != 1 and abs(head_tail[bb]-head_tail[bb+1]) != 1:
            c.append(head_tail[bb])
indexes = []
for cc in c:
    for index in range(len(ope_num)):
        if sum(ope_num[:index])>cc:
            indexes.append(index)
            break'''

job_all = {}  # 零件任务集合，字典形式{任务：工序列表}
# no_l = []
for j in range(len(ope_num)):  # 任务遍历len(ope_num)=len(no_before)
    if j == 0:
        job_all[no_after[j]] = values[:ope_num[j]]  # 第一个零件的工序集合为所有集合的前序号个
        # no_l.append(l[:ope_num[j]])
    else:
        job_all[no_after[j]] = values[sum(ope_num[:j]):sum(ope_num[:j+1])]  # 之后的工序数计算方式
        # no_l.append(l[sum(ope_num[:j]):sum(ope_num[:j+1])])
'''for nono in range(len(no_l)):
    if len(no_l[nono])>2:
        if no_l[nono][-1] < no_l[nono][-2]:
            print(nono)
            print(no_before[nono]) # 出错零件（缺少工序3）
            break'''
# print(job_all.keys())
# 包含所有零件而非产品的加工过程和时间位置等信息


