import json
# from lxml import etree

# 丁香园

with open('yiqing1.json', 'r') as f:

    jsonlist= json.loads(f.read())


# print(type(jsonlist))
for pro_dict in jsonlist:
    print('省份：\n', pro_dict['provinceName'],  ' 确诊：', pro_dict['confirmedCount'], '  治愈：', pro_dict['curedCount'], '  死亡:', pro_dict['deadCount'])
    provinceName = pro_dict['provinceName']
    confirmedCount = pro_dict['confirmedCount']
    curedCount = pro_dict['curedCount']
    deadCount = pro_dict['deadCount']
    for city in pro_dict['cities']:
        print(city['cityName'], ' 确诊：', city['confirmedCount'], '  治愈：', city['curedCount'], '  死亡:', city['deadCount'])

    








