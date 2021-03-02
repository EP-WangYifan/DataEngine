# -*- coding: utf-8 -*-
"""
黑马训练营 L3 Action: 汽车消费城市划分
数据集：car_data.csv
31个省份地区，4个维度的指标（人均GDP，城镇人口比重，交通工具消费价格指数，百户拥有汽车量）
Thinking：将城市划分为几组，哪些城市会是在一组？
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

#读取原始数据,获取除省市名外的数据训练集
RawData = pd.read_csv("car_data.csv", encoding = "gbk")
TrainData = RawData.iloc[:,1:5]

#数据规范化至[0，1]区间
TrainData = MinMaxScaler().fit_transform(TrainData)

#K-Means手肘法判断聚类数
sse=[]  #误差
for k in range(1,11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(TrainData)
    # 计算inertia簇内误差平方和
    sse.append(kmeans.inertia_)

x = range(1, 11)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()

#选择聚类数 = 4,将分类结果添加至源数据内
kmeans = KMeans(n_clusters=4).fit_predict(TrainData)
RawData['类别'] = kmeans
print(RawData)
RawData.to_excel('result.xlsx')

