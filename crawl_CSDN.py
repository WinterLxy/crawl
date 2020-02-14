'''
希望实现内容：
1.搜索某个东西，返回当搜索后的标题和链接
2.使用requests 模块练习
'''
import requests,re
from urllib import parse
from bs4 import BeautifulSoup

#简易版本
url = "https://so.csdn.net/so/search/s.do?"
a = input("请输入需要搜索的内容：")
data = {"q":a}
data = parse.urlencode(data)
url = url + data
req = requests.get(url)
# print(req.text)
soup = BeautifulSoup(req.text,"lxml") #利用Beautifulsoup进行网页解析
soup = soup.find_all("a",{"target":"_blank"}) #解析后利用findall函数找到对应的<a>标签，即搜索到的内容的标题所对应的地方，此处返回的是一个文档对象，仍然含有以下属性
# print(soup)
# print(type(soup))
titles = {} # 利用列表加入搜索后的结果标题和链接
###此处坑比较多，因为搜出来的结果，有加粗，因此返回的内容中带有<em>标签，本来准备用正则进行处理，后来发现直接使用string属性后，直接会把<em>过滤掉
# 1.循环遍历，利用contents属性，反馈的是tag的子节点，并返回列表形式
# 2.将返回的列表形式，判断是否有<em>属性，即搜索内容的加粗,再进行遍历提取，加入到字符串
# 3.提取对应的url,然后把获取的标题和url添加到字典中，最后打印出来
for item in soup:
    if "<em>" in str(item.contents):
        urls = item ["href"]
        title=""
        for i in item.contents:
        # print("----",i.string)
        # print(type(i.string))
        # print(i.string)
            title = title + i.string
        # print("-------",title)
        titles.update({title:urls})
print(titles)