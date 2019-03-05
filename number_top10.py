import time
import re
import random
import ssl
#import requests
from urllib import parse
import qq_init as qq
import pymongo
import  re
import matplotlib.pyplot as plt
import numpy as np
client = pymongo.MongoClient(host=qq.host, port=qq.port)
db = client[qq.db]
co=db['mood1']
#################每个人发说说的数量################
numberperson={}
total=0
for i in co.find():
    name=i['name']
    time = i['CreateTime'][:11]
    timeday=time.replace('-','')
    if int(timeday) > 20171124:
        total+=1
        numberperson[name]=numberperson.get(name,0)+1
items=list(numberperson.items())
items.sort(key=lambda x:x[1], reverse=True)
print(total)
x=[]
y=[]
for i in range(10):
    k,v=items[i]

    x.append(k)
    y.append(v)
    print('{0:<10}{1:>5}'.format(k,v))

plt.bar(np.linspace(1,10,10),y)
plt.title(u'单人说说数量排行榜前十',fontproperties='SimHei')
plt.show()