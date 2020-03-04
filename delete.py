import json
import requests
import pymysql


db = pymysql.connect('localhost', 'root', 'oooo0000', 'yiqing2020')
cursor = db.cursor()
def request_handle(url):
    '''发送请求'''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71'}
    r = requests.get(url, headers = headers, timeout= 5)
    # coding = r.apparent_encoding
    # r.encoding = coding
    return r

def parse_china_item(response):
    '''解析提取文件'''
    rdict = json.loads(response)
    # rdict = response.json()
    return rdict['data']['areaList']


        
def delete_mysql(tablename):
    '''删除项目'''
    sql = '''delete from %s where date='2020-03-04' ''' %(tablename)
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
    '''下载解析相关数据'''

    # url = 'https://server.toolbon.com/home/tools/getPneumonia'

    # r = request_handle(url)
    with open('yiqing_data/[2020-03-04]yiqing_full.json', 'r') as f:
       r = f.read()

    areaList = parse_china_item(r)
    for province in areaList:
        provinceName = province.get('provinceName')
        delete_mysql(provinceName)
    db.close()
if __name__ == '__main__':
    main()