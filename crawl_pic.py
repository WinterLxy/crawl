import requests
from urllib.request import urlretrieve,urlopen
from bs4 import BeautifulSoup
import os

url="https://588ku.com/image/yiqing.html"

def get_url(url):
    page = urlopen(url)
    soup = BeautifulSoup(page,"lxml")
    image_url=[]
    # print(soup)
    img = soup.find_all("a",{"class":"img-box"})
    print(img)
    for url in img:
        image_url.append("http:%s"%url["href"])

    return image_url

def download(urlbox):
    for image in urlbox:
        print(image)
        page = urlopen(image)
        soup = BeautifulSoup(page,"lxml")
        # print(soup)
        image = soup.find("img",{"class":"scaleImg"})
        print(image)
        image_url_download = image["src"]
        urlretrieve("http:%s"%image_url_download,"./{}.jpg".format(image["alt"]))

urlbox = get_url(url)
print(urlbox)
download(urlbox)


# img_list=[]
# for pg in img:
#     url = pg['data-original']
#     if ".jpg" in url:
#         pic_rul = url.split("!")[0]
#         print(pic_rul)
#     urlretrieve("http:%s"%pic_rul,"./{}.jpg".format(pg["title"]))


#
