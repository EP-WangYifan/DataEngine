# -*- coding: utf-8 -*-
"""
L5:购物篮词云分析
数据集：MarketBasket
下载地址：https://www.kaggle.com/dragonheir/basket-optimisation
对数据集进行词云可视化展示，可视化探索（Top10的商品有哪些）
"""
import pandas as pd
from wordcloud import WordCloud
#from nltk import word_tokenize
#import imageio

#数据读取
rawdata = pd.read_csv('./Market_Basket_Optimisation.csv',header = None)
#遍历并添加至alldata

alldata = []
for row in rawdata.iterrows():
    alldata.extend(row[1].dropna())

#获取种类及数量,输出前10位
alldata = pd.value_counts(alldata)
print('top10商品:\n', alldata[:10])

#利用nltk分词
#alldata = word_tokenize(alldata)

#导入轮廓图
#mk = imageio.imread("./Market.png")
my_cloud = WordCloud(
    background_color='white',  # 设置背景颜色  默认是black
    width=900, height=600,
    max_words=100,              # 词云显示的最大词语数量
    max_font_size=99,           # 设置字体最大值
    min_font_size=16,           # 设置子图最小值
    random_state=50,            # 设置随机生成状态，即多少种配色方案
    stopwords={''} ,            # 设置屏蔽词
#    mask = mk                  # 设置轮廓
).generate_from_frequencies(alldata)

#输出词云图
my_cloud.to_file('WordCloud_Market_Basket.png')

    
