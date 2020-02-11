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

def parse_china_item(response):
    '''解析提取文件'''
    rdict = json.loads(response)
    return rdict['data']['areaList']


        
def delete_mysql(tablename):
    '''删除项目'''
    sql = '''delete from %s where date='2020-02-10' ''' %(tablename)
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print('---------------删除成功------------')
    except:
        db.rollback()
        print('---------------不成功------------')
        db.close()
        exit()


def main():
    '''下载解析相关数据，存入mysql'''

    url = 'https://server.toolbon.com/home/tools/getPneumonia'

    # r = request_handle(url)
    with open('/Users/mac/python/yiqing2020/yiqing_data/[2020-02-09]yiqing_full.json', 'r') as f:
       r = f.read()

    rdict = json.loads(r)
    modifytime = rdict["data"]["statistics"]["modifyTime"]
    timeArray = time.localtime(modifytime/1000)

    areaList = parse_china_item(r)
    for province in areaList:
        provinceName = province.get('provinceName')
        delete_mysql(provinceName)
    db.close()
if __name__ == '__main__':
    main()