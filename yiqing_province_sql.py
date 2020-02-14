import json
import requests
import pymysql
import time

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
    '''从response中解析提取文件'''
    rdict = response.json()
    return rdict['data']['listData']

def parse_by_json(text):
    '''本地文本倒入数据库时用的解析'''
    json_dict = json.loads(text)
    return json_dict['data']['listData']

def create_table(item):
    '''创建表'''
    sql = '''CREATE TABLE province2020 (
        `num` int(4) NOT NULL AUTO_INCREMENT,
        `provinceId` int(2) DEFAULT NULL,
        `date` date DEFAULT NULL,
        `provinceName` CHAR(20) DEFAULT NULL,
        `confirmedCount` int(7) DEFAULT NULL,
        `curedCount` int(7) DEFAULT NULL,
        `deadCount` int(7) DEFAULT NULL,
        PRIMARY KEY (`num`)
        )'''
    print(sql)
    try:
        cursor.execute(sql)
        print('---------------创建MySQL_TABLE成功------------')
        insert_mysql(item)
    except:
        db.rollback()
        print('---------------创建MySQL_TABLE不成功------------')
        db.close()
        exit()

def insert_mysql(item):
    '插入数据到表'

    sql = '''INSERT INTO province2020(
        `provinceId`,
        `date`, 
        `provinceName`,
        `confirmedCount`,
        `curedCount`,
        `deadCount`
        ) VALUES('%s','%s','%s','%s','%s','%s')''' %(
        item['provinceId'],
        item['modifyTime'],
        item['provinceName'],
        item['confirmedCount'],
        item['curedCount'],
        item['deadCount']
        )
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
        print('---------------写入MySQL成功------------')
    except:
        db.rollback()
        print('---------------写入MySQL不成功------------')
        create_table(item)



def main():
    '''下载解析相关数据，存入mysql'''

    url = 'https://server.toolbon.com/home/tools/getPneumonia'
    r = request_handle(url)
    item_list = parse_china_item(r)

    # with open('/Users/mac/python/yiqing2020/yiqing_data/[2020-02-1]yiqing_full.json', 'r') as f:
    #    r = f.read()
    # item_list = parse_by_json(r)


    for item in item_list:
    #对timeArray进行格式转换
        # print(item)
        timeArray = time.localtime(item.get('modifyTime')/1000)
        item['modifyTime']= time.strftime("%Y-%m-%d", timeArray)

        insert_mysql(item)
    db.close()


if __name__ == '__main__':
    main()
