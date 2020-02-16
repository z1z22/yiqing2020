import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def xiantu1(df,x1,y1,x2,y2,title):
    '''绘制双线图'''

    #对plt进行设置,避免中文乱码,注意Mac可用的字体是Arial Unicode MS
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(14,8),dpi = 50)
    plt.plot(x1, y1,'o-',linewidth =3)
    plt.plot(x2, y2,'o-',linewidth =3)
    # plt.axis([0,34000])
    plt.title(title,fontsize = 20)

    #设置坐标轴名称
    plt.xlabel('日期',fontsize=18)
    plt.ylabel('人数',fontsize =18)

    plt.tick_params(labelsize = 10)#轴数据字体大小
    plt.xticks(rotation=-30)#旋转x轴上文字角度

    # plt.grid()#网格线

    # 设置数字标签
    for a, b in zip(x1, y1):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(x2, y2):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    plt.legend()#图例
    plt.savefig('/Users/mac/python/yiqing2020/yiqing_data/')
    # plt.show()
def main():
    df = pd.read_csv ('/Users/mac/python/yiqing2020/yiqing_data/yiqing_view.csv')
    x1,y1 = df.日期, df.确诊
    x2,y2 = df.日期, df.疑似
    title = '疑似、确诊人数曲线'

    xiantu1(df,x1,y1,x2,y2,title)





if __name__ == '__main__':
    main()