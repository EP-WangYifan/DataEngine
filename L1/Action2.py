#Action2: 统计全班的成绩

import pandas as pd
import numpy as np
score = {'语文':[68,95,98,90,80],'数学':[65,76,86,88,90],'英语':[30,98,88,77,90]}
score = pd.DataFrame(score,index=['张飞','关羽','刘备','典韦','许褚'])

print(score.describe())

score['Total'] = np.sum(score,1)
print(score.sort_values('Total', ascending=False))