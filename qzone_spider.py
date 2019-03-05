from selenium import webdriver
import time
import re
import random
import ssl
import requests
from urllib import parse
import qq_init as qq
import pymongo


class Spider(object):
    def __init__(self):
        '''
        初始化
        '''
        ssl._create_default_https_context=ssl._create_unverified_context
        self.driver=webdriver.Firefox(executable_path='D:\python\IDE\PyCharm Community Edition 2018.2.3\\bin\geckodriver.exe')
        self.driver.get('https://i.qq.com/')
        self.__username = qq.qq
        self.__password = qq.mm
        self.headers = {
            'host': 'h5.qzone.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'connection': 'keep-alive'
        }
        self.req = requests.Session()
        self.cookies = {}
        self.client = pymongo.MongoClient(host=qq.host, port=qq.port)
        self.db = self.client[qq.db]

    def login(self):
        '''
        登录、调用get_g_tk()、get_friends()函数
        '''
        '''
         法一 账号密码登录 多数情况下要求验证 关闭重启
         '''
        # self.driver.switch_to.frame('login_frame')
        # self.driver.find_element_by_id('switcher_plogin').click()
        # self.driver.find_element_by_id('u').clear()
        # self.driver.find_element_by_id('u').send_keys(self.__username)
        # self.driver.find_element_by_id('p').clear()
        # self.driver.find_element_by_id('p').send_keys(self.__password)
        # time.sleep(2)
        # self.driver.find_element_by_id('login_button').click()
        # self.driver.find_element_by_id('login_button').click()
        # time.sleep(1)
        '''
        法二 电脑挂上qq后直接点击头像登录（推荐
        '''
        self.driver.switch_to.frame('login_frame')
        time.sleep(1)
        self.driver.find_element_by_id('nick_646396839').click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        self.driver.get('http://user.qzone.qq.com/{}'.format(self.__username))
        cookie = ''
        for item in self.driver.get_cookies():
            cookie += item["name"] + '=' + item['value'] + ';'
        self.cookies = cookie
        print(cookie)
        self.get_g_tk()
        self.headers['Cookie'] = self.cookies
        self.get_friends()
        self.driver.quit()

    def get_friends_url(self):
        '''
        构造好友请求链接
        '''
        url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?'
        params = {
            'uin': self.__username,
            'ver': 1,
            'fupdate': 1,
            'action': 1,
            'g_tk': self.g_tk
        }
        url = url + parse.urlencode(params)
        return url

    def get_friends(self):
        '''
        获取全部好友
        '''
        offset, t = 0, True
        url = self.get_friends_url()
        print('rrr')
        name, qq_num = [], []
        while (t):
            url_ = url + '&offset=' + str(offset)
            page = self.req.get(url=url_, headers=self.headers)
            if ('\"end\":1' and '\"uinlist\":[]') in page.text:
                t = False
            else:
                names, qqs = re.findall('label":.*"', page.text), re.findall('"\d+"', page.text)
                for _, __ in zip(names, qqs):
                    name.append(re.sub('label":|"', '', _))
                    print(name)####
                    qq_num.append(re.sub('"', '', __))
            offset += 50
        self.name, self.qq_num = name, qq_num


    def get_g_tk(self):
        '''
        获取g_tk()
        '''
        p_skey = self.cookies[self.cookies.find('p_skey=') + 7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
        print('g_tk', h & 2147483647)
        self.g_tk = h & 2147483647

    def get_mood(self):
        '''
        构造说说请求链接
        对所有好友进行请求
        获取点赞好友信息
        正则解析
        存入数据库
        设置时长 5 秒，防封号
        '''
        peoplepa,peoplenot=0,0
        url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'sort': 0,
            'num': 20,
            'repllyunm': 100,
            'cgi_host': 'http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
            'callback': '_preloadCallback',
            'code_version': 1,
            'format': 'jsonp',
            'need_private_comment': 1,
            'g_tk': self.g_tk
        }
        url = url + parse.urlencode(params)
        for q in self.qq_num[185:]:
            t1, pos = True, 0
            x=0
            url_ = url + '&uin=' + str(q)
            black, shuoshuo = self.db['black1'], self.db['mood1']
            while(t1):
                temp=0
                url__ = url_ + '&pos=' + str(pos)
                mood = self.req.get(url=url__, headers=self.headers)
                if '\"msglist\":null' in mood.text or "\"message\":\"对不起,主人设置了保密,您没有权限查看\"" in mood.text:
                    t1 = False
                    if '\"message\":\"对不起,主人设置了保密,您没有权限查看\"' in mood.text:
                        data = {
                            'name': self.name[self.qq_num.index(q)],
                            'qq': q
                        }
                        peoplenot+=1
                        print(peoplenot)
                        black.insert_one(data)
                else:
                    #此页的所有
                    created_time = re.findall('created_time":\d+', mood.text)
                    source = re.findall('source_appid":".*?"source_name":".*?"', mood.text)
                    contents = re.findall('],"content":".*?"', mood.text)
                    forword = re.findall('fwdnum":\d+', mood.text)
                    comment_content = re.findall('commentlist":(null|.*?],)', mood.text)
                    comments = re.findall('cmtnum":\d+', mood.text)
                    pics = re.findall('","pic(_template|".*?])', mood.text)
                    like_url = 'https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?'
                    tids = re.findall('tid":".*?"', mood.text)
                    with open('./data1.txt','a') as f:
                        for _time, _source, _content, _forword, _comment_content, _comment, _pic, _tid in \
                                zip(created_time, source, contents, forword, comment_content, comments, pics, tids):
                            param = {
                                'uin': self.__username,
                                'unikey': 'http://user.qzone.qq.com/{}/mood/'.format(q)+re.sub('tid":"|"', '', _tid)+'.1',
                                'begin_uin': 0,
                                'query_count': 60,
                                'if_first_page': 1,
                                'g_tk': self.g_tk
                            }
                            #每一条shuoshuo
                            like_url = like_url + parse.urlencode(param)
                            #print(like_url)
                            like = self.req.get(url=like_url, headers=self.headers)
                            likers = like.text.encode(like.encoding).decode('utf-8')
                            #print(likers)
                            fuin, nick, sex, constellation, address = re.findall('fuin":\d+', likers), re.findall('nick":".*?"', likers), re.findall('gender":".*?"', likers), re.findall('tion":".*?"', likers), re.findall('addr":".*?"', likers)
                            infos = []
                            for _fuin, _nick, _sex, _constellation, _address in zip(fuin, nick, sex, constellation, address):
                                info = {
                                    'fuin': re.sub('fuin":', '', _fuin),
                                    'nick': re.sub('nick":"|"', '', _nick),
                                    'sex': re.sub('gender":"|"', '', _sex),
                                    'constellation': re.sub('tion":"|"', '', _constellation),
                                    'address': re.sub('addr":"|"', '', _address)
                                }
                                infos.append(info)
                            data = {
                                '_id': str(q) + '_' + str(random.random() * 10).replace('.', ''),
                                'name': self.name[self.qq_num.index(q)],
                                'CreateTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(re.sub('created_time":', '', _time)))),
                                'source': re.sub('source_appid":".*?"source_name":"|"', '', _source),
                                'content': re.sub('],"content":"|"', '', _content),
                                'comment_content': re.sub('null|commentlist":', '', _comment_content) if 'null' in _comment_content else str([(re.sub('content":"|"', '', x), re.sub('createTime2":"|"', '', y), re.sub('name":"|"', '', z), re.sub('uin":', '', zz)) for x, y, z, zz in zip(re.findall('content":".*?"', _comment_content), re.findall('createTime2":".*?"', _comment_content), re.findall('name":".*?"', _comment_content), re.findall('uin":\d+', _comment_content))]),
                                'comment': re.sub('cmtnum":', '', _comment),
                                'pic': [] if 'template' in _pic else [re.sub('url2":|"', '', i) for i in re.findall('url2":".*?"', _pic)],
                            }
                            timed = data['CreateTime'][:11]
                            timeday=int(timed.replace('-',''))
                            start=int(qq.startdata.repalce('-',''))
                            end=int(qq.enddata.replace('-',''))
                            if timeday<start or timeday>end:
                                temp=1
                                break
                            print(data['CreateTime'])
                            #print(t)
                            #print(data)
                            peoplepa+=1
                            x+=1
                            print(peoplepa)
                            if shuoshuo.insert_one(data):
                                print(peoplepa)
                                print('%s 的说说写入到数据库成功！' % self.name[self.qq_num.index(q)])
                            else:
                                with open('filed', 'a+', encoding='utf-8') as f:
                                    f.write('%s 的说说爬取失败！\n' % self.name[self.qq_num.index(q)])
                                print('%s 的说说写入到数据库成功！' % self.name[self.qq_num.index(q)])
                        if temp==1:
                            break
                        pos += 20
                        time.sleep(5)
                        f.write(q+'\n')
                        m=str(x)
                        f.write(m)
                        f.write('\n')
                    f.close()


    def get_information(self):
        '''
        构造请求，正则解析
        :return:
        '''
        url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?'
        params = {
            'vuin': self.__username,
            'fupdate': 1,
            'g_tk': self.g_tk
        }
        url = url + parse.urlencode(params)
        table = self.db['information']
        people=0
        for q in self.qq_num:
            t3 = True
            url_ = url + '&uin=' + str(q)
            while(t3):
                info = self.req.get(url=url_, headers=self.headers)
                if '\"message\":\"您无权访问\"' in info.text:
                    t3 = False
                else:
                    people+=1
                    text = info.text
                    sex, marriage = ['其他', '男', '女'], ['未填写', '单身', '已婚', '保密', '恋爱中']
                    constellation = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座', '未填写']
                    data = {
                        '_id': str(q) + '_' + str(random.random() * 10).replace('.', ''),
                        'nickname': re.sub('nickname":"|"', '', re.search('nickname":".*?"', text).group()),
                        'spacename': re.sub('spacename":"|"', '', re.search('spacename":".*?"', text).group()),
                        'sex': sex[int(re.sub('sex":', '', re.search('sex":\d+', text).group()))],
                        'age': re.sub('"age":', '', re.search('"age":\d+', text).group()),
                        'birthday': re.sub('birthyear":', '', re.search('birthyear":\d+', text).group()) + '-' + re.sub('birthday":"|"', '', re.search('birthday":".*"', text).group()),
                        'country': re.sub('country":"|"', '', re.search('country":".*"', text).group()),
                        'province': re.sub('province":"|"', '', re.search('province":".*?"', text).group()),
                        'city': re.sub('city":"|"', '', re.search('city":".*?"', text).group()),
                        'hometown': re.sub('hco":"|"|,|\n|hc|hp|:', '', re.search('hco":".*\n".*\n".*', text).group()),
                        'marriage': marriage[int(re.sub('marriage":', '', re.search('marriage":\d', text).group()))],
                    }
                    if table.insert_one(data):
                        print(people)
                        print('%s 信息写入到数据库成功' % self.name[self.qq_num.index(q)])
                    print(data)
                    t3 = False


sp = Spider()
sp.login()
print('登陆成功')
t = time.perf_counter()
sp.get_mood()
sp.get_information()
End = time.perf_counter() - t
print('所有内容爬取完成！总用时%s!' % End)

