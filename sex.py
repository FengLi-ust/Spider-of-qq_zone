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
#######################个人信息性别###################
inf=db['information']
bl=db['black1']
m,n=0,0
nan=0
nv=0
no=0
for i in bl.find():
    m+=1
age={}
print(m)
for i in inf.find():
    n+=1
    if i['sex']=='男':
        nan+=1
    elif i['sex']=='女':
        nv+=1
    else: no+=1
print(n)
print(nan)
print(nv)
print(no)
#调节图形大小，宽，高
plt.figure(figsize=(6,9))
#定义饼状图的标签，标签是列表
labels = [u'male',u'femal',u'unknown sex']
# #每个标签占多大，会自动去算百分比
sizes = [nan,nv,no]
colors = ['red','yellowgreen','lightskyblue']
# #将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0.1,0,0)
#
patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = True)
#
for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()
###########爬取人空间###############
#调节图形大小，宽，高
plt.figure(figsize=(6,9))
#定义饼状图的标签，标签是列表
labels = [u'not allowed 27',u'allowed 303']
# #每个标签占多大，会自动去算百分比
sizes = [27,303]
colors = ['red','yellowgreen']
# #将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0.1,0)
#
patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = True)
#
for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()