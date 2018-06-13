#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# n is the expect number of cluster
# the format of dataset is np array
import numpy as np

a = [1,0,0]
b = [1,1,0]
c = [0,1,0]
d = [1,1,1]
e = [0,0,0]
f = [0,0,1]
g = [1,0,1]
h = [0,0,1]

dataset = [a,b,c,d,e,f,g,h]
def distEclud(v1, v2):
    return np.sqrt(np.sum(np.square(v1 - v2)))

def distJaccard(s1,s2):
    length1= len(s1)
    intersect = 0
    union = 0
    for i in range(length1):
        if s1[i] != s2[i]:
            union += 1
        elif s1[i]==1 and s2[i]==1:
            union += 1
            intersect += 1
    return 1 - intersect/union

def clusterJaccardDist(cluster1,cluster2):
    min = 1000
    for item1 in cluster1:
        for item2 in cluster2:
            dis = distJaccard(item1,item2)
            if dis< min:
                min = dis

    print(cluster1,cluster2,min)
    return min

def union(cluster1,cluster2):

    return cluster1+cluster2


def hierarchyCluster(n,dataset):
    result = []
    for x in dataset:
        result.append([x])
    while(len(result) > n):
        cluster = []
        id = []
        length = len(result)
        min = 1000
        for i in range(length):
            for j in range(i + 1, length):
                distance = clusterJaccardDist(result[i], result[j])
                if (distance < min):
                    min = distance
                    cluster = union(result[i], result[j])
                    id = [i,j]
        a = result[id[0]]
        b = result[id[1]]
        result = [e for e in result if e not in (a,b)]
        result.append(cluster)
    return result
print(hierarchyCluster(4,dataset=dataset))