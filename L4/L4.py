# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:17:11 2021
购物篮分析
数据集：MarketBasket
该数据集为rawdata，没有记录TransactionID和列名
ToDo：统计交易中的频繁项集和关联规则
"""
import pandas as pd
#导入数据，并检查数据名称
rawdata = pd.read_csv('./Market_Basket_Optimisation.csv',header=None)
'''
Temp=rawdata.apply(pd.value_counts).sum(axis=1).astype(int)
pd.set_option('display.max_rows',None)
print(Temp)
#数据没有大小写问题
pd.set_option('display.max_rows',10)
'''
#使用efficient_apriori工具包
def efficient_apriori():
    from efficient_apriori import apriori
    #将rawdata中每行数据转为一个数据列，再逐行添加至transaction列中
    transaction=[]
    for i in rawdata.index:
        transaction.append(rawdata.loc[i].dropna().tolist())
    # 挖掘频繁项集和频繁规则
    itemsets, rules = apriori(transaction, min_support=0.05,  min_confidence=0.2)
    print('EA_频繁项集：', itemsets)
    print('EA_关联规则：', rules)

def mlxtend():
    #使用mlxtend.frequent_patterns工具包
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    #合并rawdata内容至一列df
    df = pd.DataFrame()
    df['Items'] = rawdata[rawdata.columns[0:]].apply(lambda x: ','.join(x.dropna()),axis=1)  
    #one-hot编码
    hot_encoded_df = df.Items.str.get_dummies(sep=",")
     # 挖掘频繁项集和关联规则
    frequent_itemsets = apriori(hot_encoded_df, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.2)
    print("MX_频繁项集：", frequent_itemsets.sort_values('support',ascending = False))
    print("MX_关联规则：", rules[ (rules['lift'] >= 1) & (rules['confidence'] >= 0.2) ])

efficient_apriori()
mlxtend()
