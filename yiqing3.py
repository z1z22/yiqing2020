import json
# from lxml import etree

# 丁香园

with open('yiqing1.json', 'r') as f:
    jsonlist= json.loads(f.read())

mylist = jsonlist[0]['cities']

with open('yiqing_new1.json', 'w') as f:
    f.write(json.dumps(mylist,ensure_ascii = False))