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
##########################说说年度词汇####################
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
# jieba.add_word('emmm',10000000)
# jieba.add_word('了解一下',1000000)
# jieba.add_word('牛逼')
#jieba.load_userdict('D:\python\Lib\site-packages\jieba\dict2.txt')
numberperson={}
words={}
eclude={'我们','一个', 'who' ,'uin' ,'nick', '自己' ,'e400824' ,'e100', '大家','今天','什么','还是','这个',
        '没有','e252','可以','现在','e105','e400101','还有','你们','e401236','这样','但是','这里','最后',
        '就是','时候','e400420','知道','这么','不要','e166','感觉','一天','e248','e400198','e400867','然后',
        '一次','怎么','觉得','已经','e113','虽然','肯定','因为','终于','不是','可能','一定','如果','他们','一直',
        '不会','e121009','e243','看到','明天','所有','e401137','u0022','e400840','所以','10','那么','e400384'
        ,'真的','一下','一起','e163','e400932','e193','小时','不能','只是','很多','e400846','东西','突然','报名',
        '一样','那个','不过','起来','以后','有人','有点','00','为了','e400837','两个','30','e400372','事情'
        ,'e282','别人','e282','e400834','e249','e139','e400351','12','e253','e144','以及','e400832','是不是',
        'e400842','个赞','一些','e401190','e400104','这种','一张','e400823','那些','e400873','the','之前','e104'
        ,'e195'}
inf=db['information']
for i in co.find():
    print(i)
    name = i['name']
    time = i['CreateTime'][:11]
    content=i['content']

    con=jieba.lcut(content)
    for word in con:
        if len(word)==1:
            continue
        words[word]=words.get(word,0)+1
for word in eclude:
    if words[word]:
        del(words[word])
items=list(words.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(130):
    k,v=items[i]
    print('{0:<10}{1:>5}'.format(k, v))
backgroud_Image = plt.imread('D:\python\IDE\PyCharm Community Edition 2018.2.3\python项目\\try1\\gou1.jpg')
print('1')
wc = WordCloud( background_color = 'white',    # 设置背景颜色
                 width=1500,height=1000,
                 mask = backgroud_Image,        # 设置背景图片
                 max_words = 100,            # 设置最大现实的字数
                 stopwords = STOPWORDS,        # 设置停用词
                 font_path = 'D:\python\include\Fonts\chuhei.ttf',# 设置字体格式，如不设置显示不了中文
                 max_font_size = 300,            # 设置字体最大值
                 random_state = 50,            # 设置有多少种随机生成状态，即有多少种配色方案
                 )
wc.generate_from_frequencies(words)
plt.imshow(wc)
plt.axis('off')
plt.show()

######################################################
numberperson={}
words={}
eclude={'空间','的'}
inf=db['information']
for i in inf.find():
    print(i)
    name=i['spacename']
    con=jieba.lcut(name)
    for word in con:
        words[word]=words.get(word,0)+1
for word in eclude:
    del(words[word])
items=list(words.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(130):
    k,v=items[i]
    print('{0:<10}{1:>5}'.format(k, v))
backgroud_Image = plt.imread('D:\python\IDE\PyCharm Community Edition 2018.2.3\python项目\\try1\\gou1.jpg')
print('1')
wc = WordCloud( background_color = 'white',    # 设置背景颜色
                 width=1500,height=1000,
                 mask = backgroud_Image,        # 设置背景图片
                 max_words = 100,            # 设置最大现实的字数
                 stopwords = STOPWORDS,        # 设置停用词
                 font_path = 'D:\python\include\Fonts\chuhei.ttf',# 设置字体格式，如不设置显示不了中文
                 max_font_size = 300,            # 设置字体最大值
                 random_state = 50,            # 设置有多少种随机生成状态，即有多少种配色方案
                 )
wc.generate_from_frequencies(words)
plt.imshow(wc)
plt.axis('off')
plt.show()