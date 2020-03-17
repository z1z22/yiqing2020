from datetime import date
import re
import requests
# from lxml import etree

def request_handle(url):
    '''发送请求'''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71'}
    r = requests.get(url, headers = headers, timeout= 5)
    coding = r.apparent_encoding
    r.encoding = coding
    return r

def parse_area(text):
    '''正则解析提取文件'''

    pattern = re.compile(r'<script id="getAreaStat">try (.*?)</script>')

    area = pattern.findall(text)[0].replace('{ window.getAreaStat = ','').replace(r'}catch(e){}','')
    return area   

def parse_country(text):
    '''正则解析提取文件'''

    pattern = re.compile(r'<script id="getListByCountryTypeService2">try (.*?)</script>')

    country = pattern.findall(text)[0].replace('{ window.getListByCountryTypeService2 = ','').replace(r'}catch(e){}','')
    return country


def create_file(path,string):

    with open(path,'w') as ft:
        ft.write(string)


def main():

    url = (
    'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other',#
    'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    )


    # r = request_handle(url[0])

    # area = parse_area(r.text)
    # path_area = f'./yiqing_data/[{date.today()}]yiqing_area.json'
    # create_file(path_area, area)
    
    # print('area文件已储存')

    # country = parse_country(r.text)
    # path_country = f'./yiqing_data/[{date.today()}]yiqing_country.json'
    # create_file(path_country, country)
    # print('country文件已储存')

    r = request_handle(url[0])

    path_full = f'./yiqing_data/qq/[{date.today()}]qq_total.txt'
    create_file(path_full, r.text)
    print('qq_total文件已储存')

    r = request_handle(url[1])

    path_full = f'./yiqing_data/qq/[{date.today()}]qq_today.txt'
    create_file(path_full, r.text)
    print('qq_today文件已储存')



if __name__ == '__main__':
    main()
