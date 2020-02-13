import requests
import pymysql
import time, json


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
    rdict = response.json()
    return rdict['data']['statistics']

def parse_by_json(text):
    json_dict = json.loads(text)
    return json_dict['data']['statistics']


def create_table(item):
    '''创建表'''
    sql = '''CREATE TABLE `china2020` (`num` int(4) NOT NULL AUTO_INCREMENT,
                             `date` date DEFAULT NULL,
                             `confirmedCount` int(7) DEFAULT NULL,
                             `suspectedCount` int(7) DEFAULT NULL,
                             `curedCount` int(7) DEFAULT NULL,
                             `deadCount` int(7) DEFAULT NULL,
                             `seriousCount` int(7) DEFAULT NULL,
                             PRIMARY KEY(`num`)
                             ) '''

    print('插入sql语句',sql)
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

    sql = '''INSERT INTO china2020(
        date, 
        suspectedCount,
        confirmedCount,
        curedCount,
        deadCount,
        seriousCount
        ) VALUES('%s','%s','%s','%s','%s','%s')''' %(
        item['modifyTime'],
        item['suspectedCount'],
        item['confirmedCount'],
        item['curedCount'],
        item['deadCount'],
        item['seriousCount'],

        )
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
        print('---------------写入MySQL成功------------')
    except:
        db.rollback()
        print('---------------写入MySQL不成------------')
        create_table(item)
    db.close()



def main():
    '''官方在2月13日修改了借口数据结构，删除了每日增长数据，增加了各地现有确诊人数,
    2月13日后使用次文件爬取'''

    url = 'https://server.toolbon.com/home/tools/getPneumonia'

    r = request_handle(url)
    item = parse_china_item(r)

    # with open('./yiqing_data/[2020-02-10]yiqing_full.json', 'r') as ft:
    #     r = ft.read()
    # item = parse_by_json(r)

    #对timeArray进行格式转换
    timeArray = time.localtime(item.get('modifyTime')/1000)
    item['modifyTime']= time.strftime("%Y-%m-%d", timeArray)

    insert_mysql(item)


if __name__ == '__main__':
    main()
