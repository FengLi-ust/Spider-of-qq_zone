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
##################有特点的说说#########################
ainum=0
birth=0
xuexi=0
lei=0
for i in co.find():
    #print(i)
    comment=i['comment_content']
    content=i['content']
    #秀恩爱#
    if re.search(r'999',comment) or re.search(r'9999',comment) or re.search(r'99999',comment):
        ainum+=1
        print(ainum)
        print(comment)

    #生日#
    if re.search(r'生日快乐',comment) or re.search(r'生快',comment) or re.search(r'日了快生',comment):
        birth += 1
        print(birth)
        print(comment)
    #学习

    if re.search(r'学习',content) or re.search(r'考',content) or re.search(r'学霸',content):
        xuexi += 1
        print(xuexi)
        print(content)
zhuan=0
to=0
for i in co.find():
    content=i['content']
    if re.search(r'转发',content) :
        zhuan+=1
    if re.search(r'投票',content):
        to+=1
print(to)
y=[ainum,birth,xuexi,zhuan]
plt.bar(np.linspace(1,4,4),y)
plt.title(u'特点突出的说说',fontproperties='SimHei')
plt.xticks([1.0,2.0,3.0,4.0],['秀恩爱','生日祝福','学习和考试','转发和投票' ],rotation=45,fontproperties='SimHei' )
plt.show()