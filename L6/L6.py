# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:12:05 2021

JetRail高铁的乘客数量预测
数据集：jetrail.csv
根据过往两年的数据（2012 年 8 月至 2014 年 8月,
需要用这些数据预测接下来 7 个月的乘客数量
以每天为单位聚合数据集

"""

import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt

#数据加载
rawdata = pd.read_csv('./jetrail.csv')

#编辑Datetime的格式,只保留日期
rawdata['Datetime'] = rawdata['Datetime'].str.split(' ',expand = True)
rawdata['Datetime'] = pd.to_datetime(rawdata['Datetime'], format='%d-%m-%Y').dt.date

#按日期聚合
rawdata = rawdata.drop('ID',axis =1)
train = rawdata.groupby('Datetime').sum()
train['ds'] = train.index
train['y'] = train['Count']
train = train.drop('Count',axis =1)


#搭建模型
model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
model.fit(train)
#预测未来7个月的数据
Future_7mons = model.make_future_dataframe(periods=213)
forcast = model.predict(Future_7mons)

plt(forcast)