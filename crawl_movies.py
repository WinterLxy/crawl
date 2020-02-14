'''
####python练习3 --爬取电影天堂####
#1. 需要实现的功能：输入电影名称后，直接出来下载链接，如果没有，则提示无此电影
#2. 可以尝试使用下载模块urllib.request.urlretrieve
#3. urllib.error模块的使用（待会可以尝试找下requests模块是否有对应的处理模块）
#4. cookie和proxy 的使用下一次模拟
'''
from urllib import request,parse,error
from bs4 import BeautifulSoup
class crawl():
    def movie_search(self):
        url = "http://s.ygdy8.com/plus/so1.php?" #分析网页发现，此网站搜索可以通过url加上搜索的数据完成，但是搜索的数据的编码并非utf-8，可以在http://web.chacuo.net/charseturlencode上边尝试编码的方式
        a = str(input("请输入要下载的电影名:"))
        data = {"typeid":"1",
                "keyword":a}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9"}
        url = url + parse.urlencode(data,encoding="gb2312")
        print(url)
        # rsp =requests.get(url)
        try:
            req = request.Request(url,headers=headers)
            rsp = request.urlopen(req).read().decode('gbk',errors='ignore')#查看网页编码为gb2312，此处使用gb2312解码，发现无法成功解，使用gbk正常,但是gbk也会出问题，加上ignore参数
        except error.URLError as e:
            print(e)
            print("解析失败")
        else:
            print("网页解析成功")
            soup = BeautifulSoup(rsp,"lxml")
            name = soup.find_all("td",{"width":'55%'})#找到对应的搜索后的电影的标签
            name_url={}
            for i in name:
                # print(i.text,"----",i.b.a["href"])
                movie_name = i.text
                movie_url = "http://s.ygdy8.com/" + i.b.a["href"]
                name_url.update({movie_name:movie_url})
            print(name_url)
a=crawl()
a.movie_search()
