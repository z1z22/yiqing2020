import json
import requests
import pymysql
import time
from datetime import date


db = pymysql.connect('localhost', 'root', 'oooo0000', 'yiqing2020')
cursor = db.cursor()
def request_handle(url):
    '''发送请求'''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71'}
    r = requests.get(url, headers = headers, timeout= 5)
    coding = r.apparent_encoding
    r.encoding = coding
    return r


def create_table(item,tablename):
    '''创建表'''
    sql = '''CREATE TABLE %s (
        `num` int(4) NOT NULL AUTO_INCREMENT,
        `date` date NOT NULL,
        `cityName` CHAR(20),
        `confirmedCount` int(7) DEFAULT NULL,
        `curedCount` int(7) DEFAULT NULL,
        `deadCount` int(7) DEFAULT NULL,
        `locationId` int(6) NOT NULL,
        `provinceId` int(2) NOT NULL,
        PRIMARY KEY (`num`)
        )''' %(tablename)
    try:
        cursor.execute(sql)
        print('---------------创建MySQL_TABLE成功------------')
        insert_mysql(item, tablename)
    except:
        db.rollback()
        print('---------------创建MySQL_TABLE不成功------------')
        db.close()
        exit()
        


def insert_mysql(item, tablename):
    '''插入数据到表'''

    sql = '''INSERT INTO %s(
        `date`, 
        `cityName`,
        `confirmedCount`,
        `curedCount`,
        `deadCount`,
        `locationId`,
        `provinceId`
        ) VALUES ('%s','%s','%s','%s','%s','%s','%s')''' %(
        tablename,
        item['modifyTime'],
        item['cityName'],
        item['confirmedCount'],
        item['curedCount'],
        item['deadCount'],
        item['locationId'],
        item['provinceId']
        )
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
        print('---------------写入MySQL成功------------')
        # db.close()
    except:
        db.rollback()
        print('---------------写入MySQL不成功------------')
        create_table(item, tablename)




def main():
    '''下载解析相关数据，存入mysql'''

    url = 'https://server.toolbon.com/home/tools/getPneumonia'

    r = request_handle(url)
    rdict = r.json()

    # with open('/Users/mac/python/yiqing2020/yiqing_data/[2020-02-09]yiqing_country.json', 'r') as f:
    #    r = f.read()
    # rdict = json.loads(r)

    modifytime = rdict["data"]["statistics"]["modifyTime"]
    timeArray = time.localtime(modifytime/1000)

    areaList = rdict['data']['areaList']
    for province in areaList:
        provinceName = province.get('provinceName')
        provinceId = int(province.get('locationId'))//10000
        for city in province.get('cities'):
            city['modifyTime'] = time.strftime("%Y-%m-%d", timeArray)
            city['provinceId'] = provinceId
            # print(city)
            insert_mysql(city, provinceName)
    db.close()

if __name__ == '__main__':
    main()
