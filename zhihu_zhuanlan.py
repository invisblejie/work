'''
   一个从知乎专栏文章关注的用户关注的专栏来获得高品质专栏

Author: visable
version: 0.0.1
editor: sublime3
time: 2016.08.30
'''

import requests
import re
import json
import time
import traceback
from bs4 import BeautifulSoup
import pymongo
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GetZhuanLan(object):

    def __init__(self, zhuanlan_name, proxy = False,page =0, time_limit = 0 ):
        self.zhuanlan_name = zhuanlan_name
        self.time_limit = time_limit
        self.start_time = time.time()
        self.url_zhihu = "https://www.zhihu.com/"
        self.url_zhuanlan = "https://zhuanlan.zhihu.com/"
        self.header = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding":"gzip, deflate, sdch",
                        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                        "DNT":"1",
                        "Connection":"keep-alive",
                        "Host":"www.zhihu.com",
                        "Upgrade-Insecure-Requests":"1",
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"}
        self.proxies = {'http': 'http://127.0.0.1:8087'}
        self.s_people   = requests.Session()
        self.s_zhuanlan = requests.Session()
        self.Ip_change_time = 0
        self.page = page
        self.need_IP = proxy
        self.zhuanlan = {}
        self.person = {}
        self.person_collection = pymongo.MongoClient().my_zhihu_database.person_collection
        self.zhuanlan_collection = pymongo.MongoClient().my_zhihu_database.zhuanlan_collection



    def start(self):
        self.login(self.s_people,self.header,"abc987","ujefdmsm@sharklasers.com",self.need_IP) # lfvzqbzz@sharklasers.com ujefdmsm@sharklasers.com rrygyidy@sharklasers.com btgrktri@sharklasers.com
        self.login(self.s_zhuanlan,self.header,"abc987","lfvzqbzz@sharklasers.com",self.need_IP)
        header = {"Host":"zhuanlan.zhihu.com"}
        self.s_zhuanlan.headers.update(header)
        self.test_database()
        self.start_time = time.time()
        self.page = int(input("wait for confirm,download start_page"))
        self.get_follow(self.zhuanlan_name)

    def test_database(self):
        print("check data")
        print("check duplicate person")
        for i in self.person_collection.find():
            if i["person_hash"] in self.person:
                print("have duplicate person", i["person_name"],i["person_hash"]," fix")
                self.person_collection.delete_one({"person_hash": i["person_hash"]})
            else:
                self.person[i["person_hash"]] = i["person_focuszhuanlan"]

        print("check duplicate zhuanlan")
        for i in self.zhuanlan_collection.find():
            if i["zhuanlan_name"] in self.zhuanlan:
                print("have duplicate zhuanlan", i["zhuanlan_name"],"  fix")
                duplicate_id = self.zhuanlan_collection.find({"zhuanlan_name":i["zhuanlan_name"]})[1]['_id']
                self.zhuanlan_collection.delete_one({"_id": duplicate_id})
            else:
                self.zhuanlan[i["zhuanlan_name"]] = i["follow_person"]["persons_hash"]

        print("check zhuanlan duplicate followers")
        for i in self.zhuanlan_collection.find():
            if (len(i["follow_person"]["persons_hash"]) != len(set(i["follow_person"]["persons_hash"]))):
                print(i["zhuanlan_name"],"have duplicate followers ,fix")
                self.zhuanlan_collection.update({"zhuanlan_name":i["zhuanlan_name"]}, {"$set" :{"follow_person.persons_hash":list(set(i["follow_person"]["persons_hash"])) ,"follow_person.persons_number":len(set(i["follow_person"]["persons_hash"]))}})

            if (len(i["follow_person"]["persons_hash"]) != i["follow_person"]["persons_number"] ):
                print(i["zhuanlan_name"],"have persons  number problem,fix")
                self.zhuanlan_collection.update({"zhuanlan_name":i["zhuanlan_name"]}, {"$set" :{"follow_person.persons_number":len(set(i["follow_person"]["persons_hash"]))}})
            
                
        print("check person duplicate focus")
        for i in self.person_collection.find():
            if len(i['person_focuszhuanlan']) != len(set(i['person_focuszhuanlan'])):
                print(i['person_name'],i["person_hash"],"have duplicate focus,fix")
                self.person_collection.update({"person_hash":i["person_hash"]}, {"$set" :{'person_focuszhuanlan':list(set(i['person_focuszhuanlan'] ))}})
        
        print("check person in focus zhuanlan")
        for i in self.person:
            for j in self.person[i]:
                if (j not in self.zhuanlan) or (i not in self.zhuanlan[j]):
                    if j not in self.zhuanlan:
                        print("person_problem",i,"missing zhuanlan", j, "fix missing zhuanlan")
                        self.get_basic(j)
                        self.zhuanlan[j] = [i]
                    self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$push":{"follow_person.persons_hash":i}})
                    self.zhuanlan_collection.update({"zhuanlan_name":j},{"$inc":{"follow_person.persons_number":1}})
                    self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$set" :{"time": time.time(),"localtime":time.strftime('%X %x %Z')}})
                    if i not in self.zhuanlan[j]:
                        print("zhuanlan_problem ", j," missing follow ", i,"    fix zhuanlan missing follower")
                        self.zhuanlan[j].append(i)

        print("check zhuanlan in follows")
        missing_follow = []
        missing = False
        for i in self.zhuanlan:
            for j in self.zhuanlan[i]:
                if j not in self.person:
                    print("person_problem",i,"zhuanlan followers missing",j )
                    missing_follow.append(j)
                    missing = True
            if missing:
                print("fix problem zhuanlan followers missing",missing_follow)
                missing = False
                new_follow = list(set(self.zhuanlan[i]) - set(missing_follow))
                self.zhuanlan_collection.update({"zhuanlan_name":i["zhuanlan_name"]}, {"$set" :{"follow_person.persons_hash":new_follow ,"follow_person.persons_number":len(new_follow)}})
                self.zhuanlan[i] = new_follow
                
        print("Caculate the existing data number")
        number_zhuanlan = self.zhuanlan_collection.find().count()
        number_person   = self.person_collection.find().count()
        focus_time_from_person = 0
        for i in self.person_collection.find():
            focus_time_from_person += len(i['person_focuszhuanlan'])
        focus_time_from_zhuanlan_from_name = 0
        focus_time_from_zhuanlan_from_number = 0
        for j in self.zhuanlan_collection.find():
            focus_time_from_zhuanlan_from_name += len(j['follow_person']["persons_hash"])
            focus_time_from_zhuanlan_from_number += j['follow_person']['persons_number']
        if  focus_time_from_person == focus_time_from_zhuanlan_from_name == focus_time_from_zhuanlan_from_number:
            print("zhuanlan: ", number_zhuanlan, "  persons:", number_person, "  total:" , focus_time_from_person)

        else:
            input("have caculate problem need fix")       
        print("data has been checked")


    def login(self, s, header, password, email, need_proxies = False):
        if need_proxies:
            s.verify = False
            s.proxies.update(self.proxies)
        s.headers.update(header)
        time.sleep(self.time_limit)
        r1 = s.get("http://www.zhihu.com/")
        if r1.status_code == 200:
            data_xsrf = s.cookies.get_dict()["_xsrf"]
            login_data = {"_xsrf": data_xsrf,
                          "password": password,
                          "remember_me":"true",
                          "email": email}
            time.sleep(self.time_limit)
            r2 = s.post("https://www.zhihu.com/login/email", data = login_data)
            if r2.status_code == 200 and json.loads(r2.text)['r'] == 0:
                print (email,"  登录成功")
                return
            while True:
                captcha_url  = self.url_zhihu +'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'
                captcha_picture = s.get(url = captcha_url)
                with open("验证码.jpeg",'wb') as f:
                        f.write(captcha_picture.content)
                login_data["captcha"] = input("验证码: ")
                time.sleep(self.time_limit)
                r2 = s.post("https://www.zhihu.com/login/email",data = login_data)
                if r2.status_code == 200 and json.loads(r2.text)['r'] == 0:
                    print (email,"  登录成功")
                    break



    def get_basic(self,zhuanlan_name):
        try:
            time.sleep(self.time_limit)
            zhuanlan_url = self.url_zhuanlan + "api/columns/" + zhuanlan_name
            basic = self.s_zhuanlan.get(zhuanlan_url)
            articles_url =  self.url_zhuanlan + "api/columns/" + zhuanlan_name + "/posts?limit=20"
            article = self.s_zhuanlan.get(articles_url)
            if basic.status_code == 200 and article.status_code == 200:
                a = json.loads(basic.text)
                focus = [[i['name'],i['postsCount']] for i in a['postTopics']]
                focus.sort(key = lambda x: -x[1])
                url = [ self.url_zhuanlan + a['slug'] ]
                description = [ a[ 'description'] ]
                followersCount = [ a['followersCount'] ]
                creator = [a['creator']['name'] , a['creator']['bio'] , a['creator']['profileUrl'] , a['creator']['description']]
                articles = [ [i['title'], self.url_zhuanlan + i['url'] , i['content']] for i in json.loads(article.text)]
            else:
                print(basic.status_code,article.status_code)
            zhuanlan_basic = {"zhuanlan_name":zhuanlan_name, "creator_name":a['creator']['name'], "creator_bio":a['creator']['bio'], "creator_description":a['creator']['description'],
                              "creator_profileUrl":a['creator']['profileUrl'], "articles": articles,"focus":focus, "followersCount":followersCount, "follow_person":{"persons_number":0,"persons_hash":[]},
                              "time":time.time(),"localtime":time.strftime('%X %x %Z')}
            self.zhuanlan_collection.insert(zhuanlan_basic)
            self.zhuanlan[zhuanlan_name] = []
            print(zhuanlan_name, time.strftime('%X %x %Z'))
        except Exception as exc:
                print(zhuanlan_name,a)
                print (traceback.format_exc() + "\n\n")
                raise
        

    def get_follow(self, zhuanlan_name):
        try:
            while True:
                if time.time() - self.start_time > 1200:
                    self.Ip_change_time += 1
                    self.change_Ip()
                    print(self.Ip_change_time)
                    self.start_time = time.time()
                time.sleep(self.time_limit)
                follow = self.s_zhuanlan.get(self.url_zhuanlan + "api/columns/" + zhuanlan_name + "/followers?limit=20&offset={0}".format(self.page), timeout=None)
                follows =  [ [ i['avatar']['id'], i['name'], i['hash'], i['profileUrl'],i['bio'],i['description'] ] for i in json.loads(follow.text)]
                for i in follows:
                    if i[2] in self.person:
                        continue
                    focus_zhuanlan,person_page = self.get_zhuanlan(i[3])
                    if len(focus_zhuanlan) != len(set(focus_zhuanlan)):
                        print(i[1], "have duplicate focus,fix")
                        focus_zhuanlan = list(set(focus_zhuanlan))
                    self.person[i[2]] = focus_zhuanlan
                    if focus_zhuanlan == []:
                        print(i[1], "作弊")
                        continue
                    person_basic = { "person_hash":i[0],"person_name":i[1], "person_hash":i[2],"person_url":i[3], "person_bio":i[4], "person_description":i[5],
                                     "person_focuszhuanlan":focus_zhuanlan, "person_page":person_page, "time":time.time(), "localtime":time.strftime('%X %x %Z')}
                    self.person_collection.insert(person_basic)
                    print(i[1], focus_zhuanlan, time.strftime('%X %x %Z'))
                    for j in focus_zhuanlan:
                        if j not in self.zhuanlan:
                            self.get_basic(j)
                            
                        self.zhuanlan[j].append(i[2])     
                        self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$push":{"follow_person.persons_hash":i[2]}})
                        self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$inc":{"follow_person.persons_number":1}})
                        self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$set" :{"time": time.time(),"localtime":time.strftime('%X %x %Z') }})
                        
                if len(follows) < 20:
                    print("finish", time.strftime('%X %x %Z'))
                    break
                if (self.page % 500) == 0:
                    print("--------have check  ", self.page, " follows------------")
                    time.sleep(10)
                self.page += 20
        except Exception as exc:
                print(json.loads(follow.text))
                print (traceback.format_exc() + "\n\n")
                raise

    def change_Ip(self):
        header = {'Host': '192.168.1.1',
                  'Referer': 'http://192.168.1.1/userRpm/StatusRpm.htm',
                  'Cookie': 'Authorization=Basic%20YWRtaW46MTIzNDU2; ChgPwdSubTag='}
        stop_url = 'http://192.168.1.1/userRpm/StatusRpm.htm?Disconnect=%B6%CF%20%CF%DF&wan=1'
        print("need to change IP")
        ip_before = requests.get('http://jsonip.com',proxies = self.proxies)
        print("IP now: ",  ip_before.json()['ip'], "Start to change IP")
        input("You need to change IP")
        while True:
            time.sleep(1)
            try:
                ip_after = requests.get('http://jsonip.com',proxies = self.proxies)
                if ip_after.json()['ip'] != ip_before.json()['ip']:
                    print("IP now: ", ip_after.json()['ip'], "Have changed IP")
                    break
                print("IP now: ", ip_after.json()['ip'])
            except:
                print("Cannot connect now")
            input("IP have problem,still need to change")

    def get_zhuanlan(self,person_url):
        try:
            time.sleep(self.time_limit)
            follow_url = person_url + "/columns/followed"
            person = self.s_people.get(url = follow_url)
            person_page = person.text
            w = BeautifulSoup(person.text,"html.parser")
            zhuanlan_name = [i.get('href')[26:] for i in w.find_all("a", attrs={"class": "zm-list-avatar-link"})]
            try:
                information = json.loads(w.find('div',attrs={"class": "zh-general-list clearfix"}).get('data-init'))
            except:
                with open("作弊.text",'a') as f:
                    f.write(follow_url + "\n")
                return ([],0)
                
            while len(zhuanlan_name) >= 20:
                information["params"]["offset"] += 20
                header = {"X-Xsrftoken":[i[1] for i in self.s_people.cookies.items()  if i[0] == "_xsrf"][0]}
                payload = {"method":"next","params":json.dumps(information["params"])}
                next_url = "https://www.zhihu.com/" + "node/" + information["nodename"]
                time.sleep(self.time_limit)
                r = self.s_people.post(url = next_url,headers = header, data = payload)
                r_person = json.loads(r.text)
                if r_person["r"] != 0:
                    raise "problem 4"
                else:
                    zhuanlan_more = [j[(j.index("http://zhuanlan.zhihu.com/") + 26):(j.index("target")-2)] for j in r_person['msg']]
                    zhuanlan_name += zhuanlan_more
                if len(zhuanlan_more) < 20:
                    break    
            return (zhuanlan_name,person_page)
        except Exception as exc:
                print(w.prettify())
                print (traceback.format_exc() + "\n\n")
                raise


class redistribution(object):
        def __init__(self,zhuanlan,person):
                self.person_collection = pymongo.MongoClient().zhihu_database.person_collection
                self.zhuanlan_collection = pymongo.MongoClient().zhihu_database.zhuanlan_collection
                self.zhuanlan_like = zhuanlan
                self.person_like = person

        def start(self):
                print("start set init value")
                self.set_start_value()
                print("set a value zhuanlan")
                self.init_value()
                print("start estimate")
                for i in range(3):
                    self.person_estimate_from_zhuanlan()
                    self.zhuanlan_estimate_from_person()
                    print("have estimate : ",i)
                print("finish")
                        

        def set_start_value(self):
                self.person_collection.update({},{"$set":{"value":0}},multi = True)
                self.zhuanlan_collection.update({},{"$set":{"value":1}}, multi = True)

        def init_value(self):
                for i in self.person_like:
                    self.person_collection.update({"person_name":i},{"$set":{"value":10}})
                for j in self.zhuanlan_like:
                    self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$set" :{"value":10}})
                
        def zhuanlan_estimate_from_person(self):
                for i in self.person_collection.find():
                        zhuanlan_focus = i['person_focuszhuanlan']
                        zhuanlan_increase_value = (i["value"]) / (len(zhuanlan_focus))
                        for j in zhuanlan_focus:
                                self.zhuanlan_collection.update({"zhuanlan_name":j}, {"$inc" :{"value":zhuanlan_increase_value}})


        def person_estimate_from_zhuanlan(self):
                for i in self.zhuanlan_collection.find():
                        for j in i["follow_person"]["persons_name"]:
                                self.person_collection.update({"person_name":j}, {"$inc" :{'value':i["value"] }})


##redistribution(["huyou","econpaper","jingjixue","wontfallinyourlap","lswlsw","geekonomics10000"],[]).start()                      
##pymongo.MongoClient().zhihu_database.person_collection.create_index([("value",-1)])
##zhuanlan_collection = pymongo.MongoClient().zhihu_database.zhuanlan_collection.create_index([("value",-1)])
            
GetZhuanLan('wontfallinyourlap').start()
        
