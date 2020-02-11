import requests
import pymysql
import time


def request_handle(url):
    '''发送请求'''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71'}
    r = requests.get(url, headers = headers, timeout= 5)
    coding = r.apparent_encoding
    r.encoding = 'utf8'
    return r

def parse_china_item(response):
    '''解析提取文件'''
    rdict = response.json()
    return rdict['data']['statistics']
def insert_mysql(item):

    db = pymysql.connect('localhost', 'root', 'oooo0000', 'yiqing2020')
    cursor = db.cursor()


    sql = '''INSERT INTO china2020(
        date, 
        suspectedCount,
        confirmedCount,
        curedCount,
        deadCount,
        seriousCount,
        suspectedIncr,
        confirmedIncr,
        curedIncr,
        deadIncr,
        seriousIncr
        ) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' %(
        item['modifyTime'],
        item['suspectedCount'],
        item['confirmedCount'],
        item['curedCount'],
        item['deadCount'],
        item['seriousCount'],
        item['suspectedIncr'],
        item['confirmedIncr'],
        item['curedIncr'],
        item['deadIncr'],
        item['seriousIncr']
        )
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
        print('---------------写入MySQL成功------------')
    except:
        db.rollback()
        print('---------------写入MySQL不成功------------')
    db.close()



def main():
    '''下载解析相关数据，存入mysql'''

    url = 'https://server.toolbon.com/home/tools/getPneumonia'

    r = request_handle(url)
    item = parse_china_item(r)

    #对timeArray进行格式转换
    timeArray = time.localtime(item.get('modifyTime')/1000)
    item['modifyTime']= time.strftime("%Y-%m-%d", timeArray)

    insert_mysql(item)


if __name__ == '__main__':
    main()
