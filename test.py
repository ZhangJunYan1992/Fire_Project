import urllib.request
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
class Cartoon:
    def __init__(self):
        self.url = 'http://djssg.naifenwy.com/cartoon'
        self.page = int(len(self.get_cartoonlist()))#一共有多少话漫画
        self.cartoonlist = self.get_cartoonlist()#查询漫画列表
        # self.totalpages = self.get_totalpages()#查询漫画页数
        self.episode = 0 #第几话漫画
        self.title = 1 #漫画的标题
        self.titles = self.get_cartoontitle() #漫画的标题组

    def get_cartoonlist(self): #查询漫画列表
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html, "html.parser")
        cartoonlist = []
        for link in bsObj.find("div",{"class":"cartoon_list"}).findAll("a"):
            if 'href' in link.attrs:
                cartoonlist.append(link.attrs['href'])
        # print(self.titles)
        # page = int(len(cartoonlist)) #获得cartoonlist里面共有多少话漫画
        return cartoonlist

    def get_cartoontitle(self): #查询漫画列表
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html, "html.parser")
        cartoontitle = []
        for title in bsObj.find("div", {"class": "cartoon_list"}).findAll("a"):
            if 'title' in title.attrs:
                cartoontitle.append(title.attrs['title'])
        self.titles = cartoontitle
        return cartoontitle

    def get_totalpages(self): #查询漫画页数
        CartoonUrl = self.cartoonlist[self.episode]
        print(CartoonUrl)
        response = urllib.request.urlopen(CartoonUrl)
        buf = response.read()
        buf = buf.decode('UTF-8')
        pattern = re.compile('<select.*?class="select_page".*?>(.*?)</select>', re.S)
        result = re.search(pattern, buf)
        option_list = result.groups(1)
        # print(option_list)
        pattern = re.compile('<option value=.*?>(.*?)</option>', re.S)
        items = re.findall(pattern, option_list[0])
        arr = []
        for item in items:
            page_url = buf + '/' + item
            arr.append(page_url)
        totalpages = int(len(arr))
        return totalpages
    def download_Cartoon(self): #下载漫画
        a = self.get_totalpages()
        i=0
        b=2
        CartoonUrl = self.cartoonlist[self.episode]
        # print(CartoonUrl)
        pattern = re.compile('(.*?)\.html', re.S)
        DownloadUrl = re.findall(pattern, CartoonUrl)
        DownloadUrl = ''.join(DownloadUrl)
        while b<a:
            url = DownloadUrl+'_'+str(b)+'.html'
            print(url)
            response = urllib.request.urlopen(url)
            buf = response.read()
            buf = buf.decode('UTF-8')
            listurl = re.findall(r'src=.+\.jpg', buf)
            listurl = re.findall(r'http:.+\.jpg', buf)
            # print(listurl)
            for url in listurl:
                f = open(r"E:\downloads" + '/'+str(self.title)+ '/' + str(i) + '.jpg', 'wb')
                req = urllib.request.urlopen(url)
                buf = req.read()
                f.write(buf)
                i += 1
            b +=1
    def DownAllCartoon(self):
        while self.episode < self.page:
            self.create_dir_path()
            self.download_Cartoon()
            self.episode +=1

    def create_dir_path(self):
        # 以漫画名创建文件夹
        changetitle = self.titles[int(self.episode)]
        self.title = changetitle.replace(':',' ')
        path = 'E:\downloads'+ '/'+str(self.title)
        exists = os.path.exists(path)
        if not exists:
            print
            "创建文件夹"
            os.makedirs(path)
        else:
            print
            "文件夹已存在"
Cartoon = Cartoon()
Cartoon.DownAllCartoon()