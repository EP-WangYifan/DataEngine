import pandas as pd

'''
# Stat_BP:  按品牌统计问题
# Stat_MP:  按车型统计问题
# Stat_BMP: 平均车型问题
'''

# 读取csv数据，清理'problem'字段格式，至data
data = pd.read_csv('car_complain.csv')

# 拆分'problem'字段，与data合并，为data_problem
data_problem = data.drop('problem',1).join(data['problem'].str.get_dummies(','))

# 按'brand'分组，统计问题条目，为Stat_BP
Stat_BP = data_problem.groupby('brand')['id'].count().reset_index().rename(columns={'id':'ProblemCount'})
Stat_BP = Stat_BP.sort_values('ProblemCount',ascending=False)

# 按'car_model'分组，统计问题条目，为Stat_MP
Stat_MP = data_problem.groupby('car_model')['id'].count().reset_index().rename(columns={'id':'ProblemCount'})
Stat_MP = Stat_MP.sort_values('ProblemCount',ascending=False)

# 按'brand'分组，统计非重复车型数量，问题条目，为Stat_BMP
# 计算平均车型问题数，增加为'AVG_MP'列
Stat_BMP = data_problem.groupby('brand').agg({'car_model':'nunique','id':'count'}).reset_index().rename(columns={'id':'ProblemCount'})
Stat_BMP['AVG_MP'] = Stat_BMP['ProblemCount'] / Stat_BMP['car_model']
Stat_BMP = Stat_BMP.sort_values('AVG_MP',ascending=False)

print(Stat_BP,Stat_MP,Stat_BMP)


