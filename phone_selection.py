#     ########################数据分析手机###################################

import time
import re
import random
import ssl
from urllib import parse
import qq_init as qq
import pymongo
import  re
import matplotlib.pyplot as plt
import numpy as np
client = pymongo.MongoClient(host=qq.host, port=qq.port)
db = client[qq.db]
co=db['mood1']
import xlwt
workbook=xlwt.Workbook(encoding='utf-8')
booksheet=workbook.add_sheet('sheet 1')
i=1
booksheet.write(0,0,label='姓名')
booksheet.write(0,1,label='手机型号')
booksheet.write(0,2,label='时间')
workbook.save('shuoshuo.xls')
for shuo in co.find():
    print(shuo)
    booksheet.write(i,0,shuo['name'])
    booksheet.write(i,1,shuo['source'])
    booksheet.write(i,2,shuo['CreateTime'])
    i+=1
workbook.save('shuoshuo.xls')
#利用excel的筛选功能进行筛选，设备种类较多，不便直接分类
total=7190
huawei,sanxin,apple,vivo,xiaomi,meizu,Android,oppo=100*(1615+698)/total,100*21/total,100*1515/total,100*1154/total,100*552/total,100*148/total,100*667/total,100*658/total
elses=100-huawei-sanxin-apple-vivo-xiaomi-meizu-Android-oppo
#调节图形大小，宽，高
plt.figure(figsize=(6,9))
#定义饼状图的标签，标签是列表
labels = [u'HUAWEI',u'IPONE',u'VIVO',u'SANXIN',u'XIAOMI',u'MEIZU',u'Android',u'else',u'OPPO']
#每个标签占多大，会自动去算百分比
sizes = [huawei,apple,vivo,sanxin,xiaomi,meizu,Android,elses,oppo]
colors = ['red','yellowgreen','lightskyblue','blue','white','green','yellow','pink','gray']
#将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0.1,0.05,0.05,0,0,0,0,0,0)

patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = True)

for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()