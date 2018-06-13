#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2018-05-13

@Original author: fanmeng
@Edit by: Chuang YANG
'''
import numpy as np
import csv
import random


# ==================================
# Point 类:
#           一条数据就是一个点
# init 方法:
#           初始化一个点
# toVector 方法：
#           将一个点转换成向量，用于简化距离计算
# my_print 方法：
#           用于打印点的信息
# ==================================
class Point:
    def __init__(self, assists_per_minute, height, time_played, age, points_per_minute):
        self.assists_per_minute = assists_per_minute
        self.height = height
        self.time_played = time_played
        self.age = age
        self.points_per_minute = points_per_minute
        self.tag = -1   # 标签用于存储聚类过程中的临时聚类结果
        self.id = -1    # id 用于存储标记点，以使得更好的展示

    def toVector(self):
        p_list = (self.assists_per_minute, self.height, self.time_played, self.age, self.points_per_minute)
        return np.array(p_list)

    def my_print(self):
        print(self.id,self.assists_per_minute, self.height, self.time_played, self.age, self.points_per_minute)

# ==================================
# 输入:
#        fileName: 数据文件名(含路径)
# 输出:
#        data_set: 数据集
# ==================================


def load_data_set(file_name):
    """ 将csv文件读成一个个点，存在data_set里 """
    data_set = []    # 初始化 dataSet
    csv_file = open(file_name, "r")  # 打开并读取csv文件
    data = csv.reader(csv_file)
    i = 0
    for item in data:
        i += 1
        if i > 1:
            p = Point(float(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4]))
            p.id = i-2
            data_set.append(p)
    return data_set

# ==================================================
# 输入:
#        vecA: 样本a
#        vecB: 样本b
# 输出:
#        sqrt(sum(power(vecA - vecB, 2))): 样本距离
# ==================================================


def distEclud(v1, v2):
    return np.sqrt(np.sum(np.square(v1 - v2)))

# ===========================================
# 函数：
#        get_centroids: 随机选择k个点作为初始化聚类中心
#        calculate_centroids: 计算一个聚类的聚类中心
#        get_cluster_by_tag： 根据所属聚类标签，将原始数据集分成k个聚类，聚类元素为Point
# ===========================================


def get_centroids(data_set, k):
    centroids = random.sample(data_set, k)
    return centroids


def calculate_centroids(cluster_set):
    assists_per_minute = 0
    age = 0
    height = 0
    time_played = 0
    points_per_minute = 0
    for p in cluster_set:
        assists_per_minute += p.assists_per_minute
        age += p.age
        height += p.height
        time_played+= p.time_played
        points_per_minute+= p.points_per_minute
    n = len(cluster_set)
    center_point = Point(assists_per_minute=assists_per_minute/n,
                         age=age/n,
                         height= height/n,
                         points_per_minute=points_per_minute/n,
                         time_played=time_played/n)

    return center_point


def get_cluster_by_tag(data_set,k):
    result = list()
    for i in range(k):
        cluster = list()
        result.append(cluster)
    for p in data_set:
        for i in range(k):
            if p.tag ==i :
                result[i].append(p)
                break
    return result


# ===========================================
# 输入:
#        dataSet: 数据集
#        k: 聚类个数
#        distMeas: 距离度量函数
#        createCent: 中点生成函数
# 输出:
#        centroids: 聚类中心点集合(每个元素为簇质心)
#        result: 聚类结果
# ===========================================
def k_means(data_set, k, distance=distEclud, createCent = get_centroids):

    # 初始化结果集
    result = []
    # 创建原始中点集
    centroids = createCent(data_set, k)
    # 聚类更改标记,当不更改的时候，表示聚类完成
    cluster_changed = True

    while cluster_changed:
        cluster_changed = False
        # 每个样本点加入其最近的聚类
        for p in data_set:
            minDist = float('inf')
            cluster_id = -1
            i = 0
            for c in centroids:
                v = c.toVector()
                d = distance(v1=p.toVector(), v2=v)
                if d < minDist:
                    minDist = d
                    cluster_id = i
                i += 1
            # 判断该点是否已存在该聚类中,并分配新的聚类tag
            if p.tag != cluster_id:
                cluster_changed = True
                p.tag = cluster_id

        # 更新聚类中心点
        result = get_cluster_by_tag(data_set=data_set, k=k)

        for i in range(k):
            centroids[i] = calculate_centroids(result[i])

    return result, centroids

def main():

    # 从csv载入数据集
    data_set = load_data_set("basketball.csv")
    # 用于存储最终结果的list
    final_result = []
    # 距离损失值,聚类的效果越好，距离损失值越小，默认计算方式为，每个点到其聚类中心的距离之和
    current_Min = float('inf')

    # 执行100次k-means，寻找结果局部最优的聚类划分集合
    for times in range(100):
        # 执行 k-means
        result = k_means(data_set=data_set,k=3,distance=distEclud,createCent=get_centroids)
        Cluster = result[0]  # 获取聚类集合
        centroids = result[1]  # 获取中心点集

        # 计算距离损失值，并更新聚类划分结果
        i = 0
        totalDistance = 0
        ll = []
        for cluster in Cluster:
            c = centroids[i].toVector()
            Distance = 0
            cluster_id = []
            for p in cluster:
                Distance += distEclud(p.toVector(), c)
                cluster_id.append(p.id)
            ll.append(cluster_id)
            totalDistance += Distance
            i += 1
        if totalDistance < current_Min:
            current_Min = totalDistance
            final_result = ll
        print("sample ", times,"totalDistance: ", totalDistance)
    i = 0
    print("min totalDistance: ", current_Min)
    for item in final_result:
        print("cluster id: ", i)
        print(final_result[i])
        i += 1

if __name__ == "__main__":
    main()