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
######################说说量分析########################
counterday={}
countershi={}
for i in co.find():
    time=i['CreateTime'][:11]
    timeday=time.replace('-','')
    print(timeday)
    timeshi = i['CreateTime'][11:13]
    if int(timeday)>20171124:
        #print('1')
        counterday[timeday]=counterday.get(timeday,0)+1
        countershi[timeshi]=countershi.get(timeshi,0)+1
print(counterday)
#counterday=sorted(counterday.keys())
items1=list(counterday.items())
items1.sort(key=lambda x:x[0])
print(items1)
key1=[]
valu1=[]
for i in range(len(items1)-1):
    k,v=items1[i]
    key1.append(k)
    valu1.append(v)
key1=np.linspace(1,365,365)

items2=list(countershi.items())
items2.sort(key=lambda x:x[0])
key2=[]
valu2=[]
for i in range(len(items2)):
    k,v=items2[i]
    key2.append(k)
    valu2.append(v)
keysort=items1.sort(key=lambda x:x[1])
valu1=counterday.values()
key1=list(map(int,counterday.keys()))
print(key1)
items1.sort(key=lambda x:x[1],reverse=True)
cou1=[]
for i in range(10):
    t,c=items1[i]
    cou1.append(c)
    print('{0:<14}{1:>5}'.format(t,c))
plt.plot(key1,valu1)
plt.xticks([0,50,100,150,200,250,300,350],['17-11-24','18-01-12','18-03-03','18-04-22','18-06-11','18-07-30','18-9-19','18-11-09' ],rotation=45 )
plt.title(u'2017-11-14到2018-11-24每日说说量',fontproperties='SimHei')
plt.xlabel(u'时间',fontproperties='SimHei')
plt.ylabel(u'说说量',fontproperties='SimHei')
plt.scatter([37,], [52, ], s=30,color='r')
plt.text(35,55,r'元旦',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([82,], [56, ], s=30,color='r')
plt.text(75,58,r'除夕',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([194,], [49, ], s=30,color='r')
plt.text(188,52,r'高考',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([265,], [49, ], s=30,color='r')
plt.text(259,52,r'七夕',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([304,], [54, ], s=30,color='r')
plt.text(304,56,r'中秋',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([344,], [59, ], s=30,color='r')
plt.text(330,61,r'IG夺冠',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([352,], [55, ], s=30,color='r')
plt.text(350,57,r'双十一',fontdict={'size':16,'color':'r'},fontproperties='SimHei')
plt.scatter([364,], [50, ], s=30,color='r')
plt.text(362,52,r'周末？',fontdict={'size':16,'color':'r'},fontproperties='SimHei')

plt.show()
#plt.subplot(313)
plt.plot(key2,valu2,'r')
plt.xticks(rotation=45)
plt.title(u'每小时说说量',fontproperties='SimHei')
plt.xlabel(u'时间',fontproperties='SimHei')
plt.ylabel(u'说说量',fontproperties='SimHei')

plt.show()
