import requests
from bs4 import BeautifulSoup
import random
import threading #多线程
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import  QStandardItemModel,QStandardItem
from queue import Queue
class WindowClass(QMainWindow):#使用Qt5做界面
    lock = threading.Lock()
    def get_headers(self):
        user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6']
        UA = random.choice(user_agent_list)
        headers = {'User-Agent': UA}
        return headers
    def get_movie(self,s):#获取搜索到的电影名称，和跳转的地址
        s = s.encode("gb2312")
        print(s)
        url = "https://www.dygod.net/e/search/index.php"
        data = {"show": "title",
                "tempid": "1",
                "keyboard": s}
        headers = self.get_headers()
        print(headers)
        movie_urls = {}
        try:
            rsp = requests.post(url=url, data=data, headers=headers).text
            soup = BeautifulSoup(rsp,"lxml")
            soup = soup.find_all("a",{"class":"ulink"})
            for i in soup:
                movie_name = i["title"]
                movie_url = "https://www.dygod.net/" + i["href"]
                movie_urls.update({movie_name:movie_url})
        except requests.exceptions as e:
            print(e)
        return movie_urls

    def get_url(self,url): #获取电影最终的下载链接
        print(url)
        headers = self.get_headers()
        try:
            rsp = requests.get(url=url,headers=headers).text.encode("ISO-8859-1").decode("gbk",errors='ignore') #可以利用rsp.encoding方法查看返回的编码格式，然后编码再解码
            # print(rsp)
            soup = BeautifulSoup(rsp,"lxml")
            soup = soup.find("td",{"style":"WORD-WRAP: break-word","bgcolor":"#fdfddf"})
            print("-------",soup.a["href"])
        except EXCEPTION as e:
            print(e)
            return None
        return soup.a["href"]

    def get_final(self,list_queue): #获取最终的名字和下载链接
        if not list_queue.empty():
            print("准备获取最终电影链接")
            (movie,url), = list_queue.get().items()
            finanl_url = self.get_url(url)
            final.update({movie:finanl_url})
            print(final)
            print("完成~~~~~")


    #如果集成QMainWindow 则self.setLayout(self.layout) 替换成
    """
        widget=QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
    """
    #即可， 注意集成QWidget和集成QMainWindow时候区别

    def __init__(self,parent=None):
        super(WindowClass, self).__init__(parent)
        self.resize(600,600)
        self.setWindowTitle("电影爬取")
        self.layout = QGridLayout()
        self.model=QStandardItemModel(0,2)#存储任意结构数据
        self.model.setHorizontalHeaderLabels(['搜索结果','下载链接'])
        self.label = QLabel()
        self.label.setText("电影名称：")
        self.Edit = QLineEdit()
        self.Button = QPushButton()
        self.Button.setText("搜索")
        self.Button.clicked.connect(self.click)
        self.tableView = QTableView()
        self.layout.addWidget(self.label, 0, 0, 1, 1)
        self.layout.addWidget(self.Edit, 0, 1,1,1)
        self.layout.addWidget(self.Button, 0, 2, 1, 1)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.layout.addWidget(self.tableView,1, 0, 1, 3)

        #继承QMainWidow使用下面三行代码
        widget=QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        #继承QWidget则使用下面这样代码
        #self.setLayout(self.layout)

        #设置表格充满这个布局QHeaderView
        #self.tableView.horizontalHeader().setStretchLastSection(True)#最后一列决定充满剩下的界面
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#所有列自动拉伸，充满界面

        # #添加menu菜单栏,注意：QMainWindow 才可以有菜单栏，QWidget没有，因此上面只能采用继承QMainWIndow
        # tool = self.addToolBar("File") #这里尝试使用QmenuBar，则此时会卡死，无法完成下面appedRow操作（猜测：可能是因为本身不允许menuBar完成这种操作）
        # self.action= QAction("添加", self)
        # self.action2=QAction("删除",self)
        # tool.addAction(self.action)
        # tool.addAction(self.action2)
        # tool.actionTriggered[QAction].connect(self.processtrigger)
        #
        # self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)#设置只能选中一行
        # self.tableView.setEditTriggers(QTableView.NoEditTriggers)#不可编辑
        # self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows);#设置只有行选中
    def click(self):
        print("点击按钮")
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['搜索结果', '下载链接'])
        list_queue = Queue()
        thread_list = []
        global final
        final = {}
        movie_name = self.Edit.text()
        print(movie_name)
        a = self.get_movie(movie_name)
        if a:
            for k, v in a.items():
                list_queue.put({k: v})
            for i in range(list_queue.qsize()):
                jincheng = threading.Thread(target=self.get_final, args=(list_queue,))
                print("------第{}进程-------".format(i))
                jincheng.start()
                thread_list.append(jincheng)
            for jincheng in thread_list:
                jincheng.join()
        else:
            final = {"未搜索到该电影":"-------"}
        print("搜索完成")
        print(final)
        for k, v in final.items():
            self.model.appendRow([QStandardItem(k),QStandardItem(v)])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())