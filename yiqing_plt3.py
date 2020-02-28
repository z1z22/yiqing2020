import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
#对plt进行设置,避免中文乱码,注意Mac可用的字体是Arial Unicode MS
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
engine = create_engine('mysql+pymysql://zz:asimazz@localhost:3306/yiqing2020')
protoday = pd.read_sql_table('province_today',engine)
out_hu = protoday.drop(axis =1,index =33)
plt_w = out_hu['provinceName']

plt.figure(figsize =[12,5])
plt.bar(plt_w,out_hu['confirmedCount'],width=0.5)

plt.xticks(rotation=-90)#旋转x轴上文字角度

string ='全国疫情对比'+str(out_hu['date'][1])
plt.title(string,fontsize = 30)
plt.grid()
plt.ylabel('确诊人数',fontsize=20)
plt.show()