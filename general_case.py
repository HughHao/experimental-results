# -*- coding: utf-8 -*-
# @Time : 2022/5/24 11:14
# @Author : hhq
# @File : general_case.py


import copy

import numpy as np
from read_benchmarks.read_dapfsp import Clas_data


class Allocate_Jobs:  # 吧序列中的工件依次分配到合适的工厂上
    # 得到每个工厂的工件分配情况和工厂的结束时间，
    def __init__(self, PT, f, sequence):
        self.PT = PT  # 含每个工件加工时间
        self.f = f  # 工厂数量
        self.Fact = [[] for i in range(self.f)]  # 每个工厂分配的工件集合
        self.sequence = sequence  # 给定的工件局部序列或整体序列
        self.Cmax = np.zeros(self.f)  # 目标为Cmax
        self.m = len(PT[0])  # 流水加工的机器数，无并行

    '''
    注意：可再定义每个每个工件的结束时间和每个产品的开始装配时间（即每个产品的工件全部完成时刻）
    '''

    '''
    NR1:Assign job j to the factory with the lowest current Cmax, not including job j
    '''

    # 选出当前Cmax最小的工厂
    def NR1(self):
        goal_f = np.argmin(self.Cmax)
        return goal_f

    '''
    NR2:Assign job j to the factory which completes it at the earliest time,i.e., the factory with the lowest Cmax, 
    after including job j.
    '''

    # 假如每个工厂都添加被选择工件J的情况下啊，完工时间最小的工厂为目标工厂
    def NR2(self, job):
        Sequences = [copy.copy(self.Fact[i]) for i in range(self.f)]  # 有嵌套是浅拷贝
        ft = np.zeros(self.f)
        for ff in range(self.f):
            Sequences[ff].append(job)
            S = Sequences[ff]
            CIJ = self.Cal_C(S)
            C = np.max(CIJ[:, self.m])
            ft[ff] = C
        # print(ft)
        goal_f = np.argmin(ft)
        return goal_f

    # 计算已经分配序列的完工时间Cmax，可以是局部也可以是整体
    def Cal_C(self, S):
        CIJ = np.zeros([len(S) + 1, self.m + 1])  # 每个工序的结束时间
        for i in range(1, len(CIJ)):  # 遍历工件
            for j in range(1, len(CIJ[0])):  # 遍历工序
                CIJ[i][j] = max(CIJ[i][j - 1], CIJ[i - 1][j]) + self.PT[S[i - 1]][j - 1]
        # C = np.max(CIJ[:, self.m])
        # print(CIJ[:, self.m])
        return CIJ

    def main(self, rule):  # 整体循环将完整序列的每个工件分配到各个工厂内
        for j in self.sequence:
            if rule == 1:  # 判断选择哪个规则
                goal = self.NR1()
            else:
                goal = self.NR2(j)
            # print(goal)
            self.Fact[goal].append(j)  # 将工件添加到目标工厂内
            # print(j, goal, self.Fact)
            S = self.Fact[goal]
            CIJ = self.Cal_C(S)
            C = np.max(CIJ[:, self.m])
            self.Cmax[goal] = C  # 更新该工厂的Cmax,Fact内是工厂分配的工件序列


# PT = [[10, 5], [6, 7], [8, 4], [9, 6], [3, 11]]
# sequence = [2, 4, 0, 3, 1]
# f = 2
# jobs = [[3, 4], [9, 7], [7, 5]]
# se = [0, 1, 2]
#
#
# all_f = Allocate_Jobs(PT, f, sequence)
# all_f.main(1)
# print(all_f.Fact)

'''
Heuristic2
Step1：按照FL算法对产品的工件进行局部序列排序
Step2：计算每个产品的最早装配时间Eh：将上步局部序列的工件按照NR1或NR2分配到每个工厂内，计算每个工厂的最早结束时间，即为该产品最早装配时间;
Step3：按照Eh对产品升序排序得到Pai
Step4：按照产品排序构造所有产品的工件排序
Step5：再次按照NR1或NR2将整个工件序列的工件分配到每个工厂内
'''

# Jobs_all = [[[1], [4,3]], [[5], [8,7]], [[7], [4,5]], [[9], [3,4]], [[3],
#            [6,7]], [[8], [1,4]], [[8], [1]], [[4], [3,5]], [[2], [5,6]]]
# NN = [[2, 3, 5], [0, 1, 7, 8], [4, 6]]
# MA = [6, 18, 13]


class Sort_products:  # 对产品排序，按照Heuristic2

    def __init__(self, Jobs, NN, MA):
        self.PT = Jobs
        self.NN = NN
        self.MA = MA
        self.m = 0  # 机器数量
        self.n = len(Jobs)  # 工件数量
        for j in range(len(Jobs[0])):  # 遍历第一个工件的所有工序
            self.m += len(Jobs[0][j])  # 计算每个工序包含的机器数
        self.M_end = np.zeros(self.m)  # 初始化所有机器的加工时间
        self.C_max = np.zeros(self.n)  # 每个工件的结束时间
        self.S_min = np.zeros(self.n)  # 每个工件的开始时间

    def Get_Eh(self):
        # minf = np.zeros(self.f)  # 每个产品的最早装配时间
        # all_f = Allocate_Jobs(Jobs, self.f, BS)
        # all_f.main(rule)
        # for ff in range(self.f):
        #     minf[ff] = all_f.Cmax[ff]  # 获取每个工厂的结束时间
        # Eh = min(minf)
        all_f = Allocate_Jobs(Jobs, self.f, BS)  # 把工件分配到工厂中
        CIJ, _ = all_f.Cal_C(BS)
        Eh = np.max(CIJ[:, all_f.m])
        return Eh

    def main(self, BS, Jobs):  # BS为已经排序好的每个产品的工件局部序列
        Ehs = np.zeros(len(self.NN))
        for i in range(len(self.NN)):  # 对产品遍历
            Ehs[i] = self.Get_Eh(BS[i], Jobs[i])
        sorted_products = np.argsort(Ehs)
        return sorted_products

    def main2(self, BS, Jobs, MA):
        Ehs = np.zeros(len(self.NN))
        for i in range(len(self.NN)):  # 对产品遍历
            Ehs[i] = self.Get_Eh(BS[i], Jobs[i]) + MA[i]
        sorted_products = np.argsort(Ehs)
        return sorted_products

    def main3(self, BS, Jobs, MA):
        Ehs = np.zeros(len(self.NN))
        for i in range(len(self.NN)):  # 对产品遍历
            Ehs[i] = self.Get_Eh(BS[i], Jobs[i]) / MA[i]
        sorted_products = np.argsort(Ehs)
        return sorted_products

    def main4(self, BS, Jobs, MA):
        Ehs = np.zeros(len(self.NN))
        for i in range(len(self.NN)):  # 对产品遍历
            if self.Get_Eh(BS[i], Jobs[i]) != 0:
                Ehs[i] = MA[i] / self.Get_Eh(BS[i], Jobs[i])
            else:
                Ehs[i] = 100000000000000
        sorted_products = np.argsort(Ehs)
        return sorted_products


# 计算每个产品的工件最佳排序并将其分配到合适的工厂，然后按照最早结束时间对产品排序
from Calculate import FL


def sort_jobs(PT):
    fl = FL(PT)
    fl.main()  # # 整体循环将完整序列的每个工件分配到各个工厂内
    BS = fl.BS  # 得到工件加工时间集的工件排序，置换车间
    return BS


def GetBS(Jobs_all, NN):  # 对产品按照最早装配时间排序
    # 然后对所有产品构造工件序列，再进行重分配得到各个工厂的完工时间
    BS, Jobs = [[] for i in range(len(NN))], [[] for i in range(len(NN))]
    for i in range(len(NN)):
        Jobs[i] = np.array([Jobs_all[NN[i][j]] for j in range(len(NN[i]))])  # 将工件集中对应工件返回到对应产品工件集中
        BS[i] = sort_jobs(Jobs[i])  # 获取每个产品额的最佳工件排序，不考虑并行工厂，即非分布式调度，也没有并行机器
    return BS, Jobs  # 每个产品包含的工件


def init_data():
    Jobs_all = Clas_data.pt
    NN = list(Clas_data.Ass_J.values())
    MA = Clas_data.Ass_t
    f = Clas_data.Fa_Num
    for p in range(len(NN)):
        for jj in range(len(NN[p])):
            NN[p][jj] -= 1
    return Jobs_all, NN, MA, f


Jobs_all, NN, MA, f = init_data()  # 初始化原始数据
# todo 获取每个产品的最佳工件排序
BS, Jobs = GetBS(Jobs_all, NN)  # 得到每个产品的工件最佳排序集合和相应工件集合


def S1(MA):
    return np.argsort(MA)


def S2(Jobs_all, NN, f, BS, Jobs):
    pai2 = Sort_products(Jobs_all, NN, f)
    '''至此完成heuristic2，对产品按照最早装配时间排序'''
    pai = pai2.main(BS, Jobs)  # sorted_products
    return pai


def S3(Jobs_all, NN, f, BS, Jobs, MA):
    pai3 = Sort_products(Jobs_all, NN, f)
    pai = pai3.main2(BS, Jobs, MA)  # sorted_products
    return pai


def S4(Jobs_all, NN, f, BS, Jobs, MA):
    pai4 = Sort_products(Jobs_all, NN, f)
    pai = pai4.main3(BS, Jobs, MA)  # sorted_products
    return pai


def S5(Jobs_all, NN, f, BS, Jobs, MA):
    pai5 = Sort_products(Jobs_all, NN, f)
    pai = pai5.main4(BS, Jobs, MA)  # sorted_products
    return pai


def get_pai(s):
    if s == 1:
        pai = S1(MA)
    elif s == 2:
        pai = S2(Jobs_all, NN, f, BS, Jobs)
    elif s == 3:
        pai = S3(Jobs_all, NN, f, BS, Jobs, MA)
    elif s == 4:
        pai = S4(Jobs_all, NN, f, BS, Jobs, MA)
    else:
        pai = S5(Jobs_all, NN, f, BS, Jobs, MA)
    return pai


'''rule可选1和2，分别表示两种分配规则'''
ten_results = []
for rule in range(1, 3):
    '''s可选1，2，3，4，5，表示五种装配件排序规则'''
    for s in range(1, 6):
        pai = get_pai(s)
        # print(pai)  # 产品序列

        '''完成整体序列构造'''
        # todo 构造完整序列
        total_sequence = []  # 工件集合
        for i in pai:
            for j in BS[i]:  # BS内是已经排序的工件集合，
                total_sequence.append(NN[i][BS[i][j]])

        # print(total_sequence)
        # 根据加工时间和完整序列将工件依次分配到合适的工厂再进行完工时间计算
        all_jobs_f = Allocate_Jobs(Jobs_all, f, total_sequence)
        all_jobs_f.main(rule)  # 更新工厂分配和机器时间
        Factory = all_jobs_f.Fact  # 两个工厂内工件的分布情况
        # print(Factory)
        CIJ = []
        for ff in range(f):  # 每个工厂的序列工件加工时间，由于是分布式加工，不需要考虑彼此间的影响
            CIJ.append(all_jobs_f.Cal_C(Factory[ff]))
        C_J = np.zeros(len(Jobs_all))  # 每个工件的结束时间
        for ff in range(f):
            for jj in range(1, len(CIJ[ff])):  #
                C_J[Factory[ff][jj - 1]] = np.max(CIJ[ff][jj])  #
        # 计算每个装配件的开始装配时间
        STart_ASS = np.zeros(len(MA) + 1)
        Compl_ASS = copy.copy(STart_ASS)
        for ass in range(1, len(MA) + 1):
            STart_ASS[ass] = max(C_J[NN[ass - 1]])  # 开始时间为工件最大结束时间和上一装配件的结束时间的较大值
        pai_new = np.argsort(STart_ASS)  # 新顺序
        for ass in range(1, len(MA) + 1):
            Compl_ASS[pai_new[ass]] = max(STart_ASS[pai_new[ass]], Compl_ASS[pai_new[ass - 1]]) + MA[pai_new[ass] - 1]
        # print(Compl_ASS)
        # print(max(Compl_ASS))
        ten_results.append(max(Compl_ASS))
print(ten_results)
