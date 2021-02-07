'''Action1：汽车投诉信息采集：
数据源：http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml
投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
可以采用Python爬虫，或者第三方可视化工具
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
   
# 得到页面的内容
def getcontent(url):   

    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

#投诉信息解析
def analysis(soup):
    #ComplainList: 目标表格
    #ComplainNm: 列名称
    #ComplainRow: 行内容
    
    #根据表头创建抱怨问题ComplainList
    ComplainNm = []
    content = soup.find('div', class_='tslb_b')
    th_list = content.find_all('th')
    for th in th_list:
        ComplainNm.append(th.text)
    ComplainList = pd.DataFrame(columns= ComplainNm)
    
    #遍历每一条tr，将td内容添加ComplainRow中，并合并到ComplainList中
    tr_list = content.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list) >0:
            ComplainRow = {}
            for i in range(0, len(td_list)):
                ComplainRow[ComplainNm[i]] = td_list[i].text
            ComplainList = ComplainList.append(ComplainRow, True)
    return ComplainList

#数据清理
def datacleaning(ComplainList):
    #TypeList: 单行切分后的问题列表
    for index, row in ComplainList.iterrows():   
        Year, Engine, Gearbox, Others = '','','',''
        TypeList = row['投诉车型'].split(' ')
        for tl in TypeList:
            if tl[-1:] == '款' and (tl[:2] == '20'):
                Year = tl[:4]  
                continue
            if tl.find('TSI') > 0 or(tl.find('.')>0 and (tl.find('T') >0 or tl.find('L') >0)):
                Engine = tl
                continue
            if tl in ['手动','自动','双离合','DSG','CVT'] :
                Gearbox = tl
                continue
            Others = Others + ' ' + tl
            
        ComplainList.loc[index, 'type_year'] = Year
        ComplainList.loc[index, 'type_Engine'] = Engine
        ComplainList.loc[index, 'type_Gearbox'] = Gearbox
        ComplainList.loc[index, 'type_Others'] = Others
       
    #ComplainList = ComplainList.drop(['投诉车型'],axis=1)
    return ComplainList

# 请求URL
url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml'
soup = getcontent(url)
datacleaning(analysis(soup)).to_excel('ComplainList.xlsx')
