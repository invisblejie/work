import requests
from bs4 import BeautifulSoup
import traceback
import re
from time import gmtime, strftime
import queue,threading
import sys
import pymongo



class secret(object):
    number = 0
    def __init__(self,URL,page,thread_number):
        self.start = page
        self.page = page
        self.URL = URL
        self.header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Accept-Encoding":"gzip, deflate, sdch",
                       "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                       "Cache-Control":"max-age=0",
                       "DNT":"1",
                       "Host":"www.sis001.com",
                       "Proxy-Connection":"keep-alive",
                       "Referer":"http://www.sis001.com/forum/forumdisplay.php?fid=230&filter=type&typeid=1225&page=2",
                       "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"}
        self.proxies = {'http': 'http://127.0.0.1:8087'}
        self.q = queue.Queue(10)
        self.thread_number = thread_number

    def worker(self):
        while True:
            item = self.q.get()
            if item is None:
                break
            self.get_download(item)
            self.q.task_done()

    def get_link(self):
        for i in range(self.thread_number):
            t = threading.Thread(target = self.worker, name = "Thread_{0}".format(i))
            t.start()
        while True:
            try:
                url = self.URL.format(self.page)
                try:
                    r = requests.get(url,proxies = self.proxies,headers = self.header, timeout = (5, 27) )
                except Exception as exc:
                    sys.stdout.write (traceback.format_exc() + "\n\n")
                    with open("E://video/torrent/error.text","a") as f:
                        f.write(url + "\n" + str(traceback.format_exc()) + "\n\n")
                if r.status_code != 200:
                    with open("E://video/torrent/error.text","a") as f:
                        f.write(r.status_code + url  + self.page +  "\n\n")
                    sys.stdout.write(r.status_code + "\n\n")
                    continue
                s = BeautifulSoup(r.content,"html.parser")
                link = [ "http://www.sis001.com/forum/" + i.get('href') for i in s.find_all(title="新窗口打开")]
                if len(link) <= 6:
                    a = input("url")
                    secret(a, 1,5).get_link()
                self.q.put([link,self.page])
                self.page += 1
            except Exception as exc:
                sys.stdout.write (traceback.format_exc() + "\n\n")
                with open("E://video/torrent/error.text","a") as f:
                    f.write(self.page + "\n" + str(traceback.format_exc()) + "\n\n")
                continue

    def get_download(self,link):
        page_now = link[1]
        link = link[0]
        for i in link:
            try:
                r = requests.get(i,proxies = self.proxies, headers = self.header, timeout = (5, 27))
                if r.status_code != 200:
                    with open("E://video/torrent/error.text","a") as f:
                        f.write(r.status_code + i  + page_now +  "\n\n")
                    sys.stdout.write(r.status_code + "\n\n")
                    continue
                s = BeautifulSoup(r.content,"html.parser")
                try:
                    number_download = [int(s(text=re.compile("下载次数"))[0][s(text=re.compile("下载次数"))[0].find("下载次数")+6:s(text=re.compile("下载次数"))[0].find("下载次数")+s(text=re.compile("下载次数"))[0][s(text=re.compile("下载次数"))[0].find("下载次数"):].find('\r')])]
                except:
                    number_download = [int(i[i.find("下载次数")+6:]) for i in s(text=re.compile("下载次数"))]
                link_download = ["http://www.sis001.com/forum/attachment." + l.get('href')[8:] for l in s.find_all(title="查看BT文件资源信息-SIS001专用")]
                comment = int(s(text=re.compile("var maxpage"))[0][s(text=re.compile("var maxpage"))[0].find('=')+1:s(text=re.compile("var maxpage"))[0].find(';')])
                page_name = s.title.string[:s.title.string.find("- Asia")]
                for j in range(len(number_download)):
                    sys.stdout.write( page_name +"\n" +  i + "\n" + "下载量: " + str(number_download[j]) + "   " +  str((min(420000 ,(100000 + self.number * 5000 - (page_now - self.start)*3000)) - min(400000,(comment - 1)*20000))) + "  " + "评论页数: " + str(comment)  +  "  " + str(page_now) + strftime("    %Y %b %d %H:%M:%S", gmtime()) + "\n\n")
                    if number_download[j] > (min(420000 ,(100000 + self.number * 5000 - (page_now - self.start)*3000)) - min(400000,(comment - 1)*20000)):
                        r_download = requests.get(link_download[j],proxies = self.proxies, timeout = (5, 27))
                        self.number += 1
                        post = {"name":page_name,"html":r.text,"torrent":r_download.content,"rank":self.number,"download":number_download[0],"date":strftime("    %Y %b %d %H:%M:%S", gmtime())}
                        collection.insert(post)
                        with open("E://video/torrent/{0}.torrent".format(self.number),'wb') as f:
                            f.write(r_download.content)
                        with open("E://video/torrent/describe.text","a") as f:
                            f.write( page_name  +  "\n"  + i + "\n" +  link_download[j]  +  "\n" + "下载量: " + str(number_download[j]) + "     评论页数：" + str(comment) + "    号码：" + str(self.number) + "\n\n")
            except Exception as exc:
                sys.stdout.write (traceback.format_exc() + "\n\n")
                with open("E://video/torrent/error.text","a") as f:
                    f.write(i + "\n" + str(traceback.format_exc()) + "\n\n")

client = pymongo.MongoClient()
db = client.secret_database
collection = db.secret_collection
secret("http://www.sis001.com/forum/forum-58-{}.html",1, 6).get_link()

