import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
#对plt进行设置,避免中文乱码,注意Mac可用的字体是Arial Unicode MS
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
engine = create_engine('mysql+pymysql://zz:asimazz@localhost:3306/yiqing2020')
df= pd.read_sql_table('yiqing_view',engine)


plt.figure(figsize=(12,5))
plt.plot(df.日期, df.确诊,'o-',linewidth =3)
plt.plot(df.日期, df.疑似,'o-',linewidth =3)
plt.plot(df.日期, df.治愈,'o-',linewidth = 3)
plt.plot( df.日期, df.死亡,'o-',linewidth = 3)
# plt.axis([0,34000])
plt.title('各项总数对比',fontsize = 20)

#设置坐标轴名称
plt.xlabel('日期',fontsize=18)
plt.ylabel('人数',fontsize =18)

plt.tick_params(labelsize = 10)#轴数据字体大小
plt.xticks(rotation=-30)#旋转x轴上文字角度

# plt.grid()#网格线

# 设置数字标签
for a, b in zip(df.日期, df.确诊):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(df.日期, df.疑似):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(df.日期, df.死亡):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(df.日期, df.治愈):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.show()