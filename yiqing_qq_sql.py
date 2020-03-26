import json
import requests
import pymysql

db = pymysql.connect('localhost', 'root', 'oooo0000', 'yiqing2020')
cursor = db.cursor()
def request_handle(url):
    '''发送请求'''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71'}
    r = requests.get(url, headers = headers, timeout= 5)
    coding = r.apparent_encoding
    r.encoding = coding
    return r

def create_table(item):
    '''创建表'''
    sql = '''CREATE TABLE dailyNewAddHistory (
        `num` int(4) NOT NULL AUTO_INCREMENT,
        `date` CHAR(10) DEFAULT NULL,
        `hubei` int(7) DEFAULT NULL,
        `country` int(7) DEFAULT NULL,
        `notHubei` int(7) DEFAULT NULL,
        PRIMARY KEY (`num`)
        )'''
    try:
        cursor.execute(sql)
        print('---------------创建MySQL_TABLE成功------------')
        insert_mysql(item)
    except:
        db.rollback()
        print('##############创建MySQL_TABLE不成功###########')
        db.close()
        exit()

def insert_mysql(sql):
    '''执行sql语句插入到mysql'''
    # print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print('---------------写入MySQL成功------------')
    except:
        db.rollback()
        print('#############写入MySQL不成功############')
        # create_table(item)

def sql_dayList(item):
    '''构建sql语句'''

    sql = f'''INSERT INTO chinaDayList_qq(
        `date`,
        `confirm`, 
        `suspect`, 
        `dead`,
        `heal`,
        `nowConfirm`,
        `nowSever`,
        `deadRate`,
        `healRate`
        ) VALUES('{item['date']}',
        '{item['confirm']}',
        '{item['suspect']}',
        '{item['dead']}',
        '{item['heal']}',
        '{item['nowConfirm']}',
        '{item['nowSevere']}',
        '{item['deadRate']}',
        '{item['healRate']}'
        )'''
    insert_mysql(sql)

def sql_foreign(item):
    '''构建sql语句'''

    sql = f'''INSERT INTO foreign_qq(
        `date`,
        `isUpdated`, 
        `name`, 
        `confirmAdd`,
        `confirm`,
        `suspect`,
        `dead`,
        `heal`
        ) VALUES('{item['date']}',
        '{item['isUpdated']}',
        '{item['name']}',
        '{item['confirmAdd']}',
        '{item['confirm']}',
        '{item['suspect']}',
        '{item['dead']}',
        '{item['heal']}'
        )'''
    insert_mysql(sql)

def sql_add(item):
    '''构建sql语句'''


    sql = f'''INSERT INTO chinaDayAdd_qq(
        `date`,
        `confirm`, 
        `suspect`, 
        `dead`,
        `heal`,
        `deadRate`,
        `healRate`
        ) VALUES(
        '{item["date"]}',
        '{item["confirm"]}',
        '{item["suspect"]}',
        '{item["dead"]}',
        '{item["heal"]}',
        '{item["deadRate"]}',
        '{item["healRate"]}'
        )'''
    insert_mysql(sql)

def sql_new(item):
    '''构建sql语句'''


    sql = f'''INSERT INTO dailyNewAddHistory(
        `date`,
        `hubei`, 
        `country`, 
        `notHubei`
        ) VALUES(
        "{item['date']}",
        "{item['hubei']}",
        "{item['country']}",
        "{item['notHubei']}"
        )'''
    insert_mysql(sql)

def main():
    '''下载qq解析相关数据，存入mysql'''

    url = ('https://view.inews.qq.com/g2/getOnsInfo?name=disease_other',
        'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign')
    r = request_handle(url[0])
    r_dict= r.json()

    # with open('yiqing_data/qq/[2020-03-04]qq_total.txt','r') as ft:
    #     r = ft.read()
    # r_dict = json.loads(r)

    data = r_dict['data']
    data_dict = json.loads(data)

    # for chinaadd in data_dict['chinaDayAddList']:
    #     insert_mysql(chinaadd)

    # for dailyNew in data_dict['dailyNewAddHistory']:
    #     insert_mysql_new(dailyNew)

    # for chinaday in data_dict['chinaDayList']:
    #     sql_dayList(chinaday)


    dayadd = data_dict['chinaDayAddList'][-1]
    sql_add(dayadd)

    dailyNew = data_dict['dailyNewAddHistory'][-1]
    sql_new(dailyNew)

    chinaday = data_dict['chinaDayList'][-1]
    sql_dayList(chinaday)



    r1 = request_handle(url[1])
    r_dict1= r1.json()

    data1 = r_dict1['data']
    data_dict1 = json.loads(data1)

    for foreign in data_dict1['foreignList']:
        sql_foreign(foreign)

    db.close()


if __name__ == '__main__':
    main()
