import requests
from bs4 import BeautifulSoup
import random
import threading #多线程
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import  QStandardItemModel,QStandardItem
from queue import Queue

'''
######分析电影天堂的电影网站#######
#1. 电影天堂的网址：https://www.dygod.net/
#2. 分析发现每次搜索，网址会直接变为https://www.dygod.net/e/search/result/?searchid=137654，带search id类型的，继续分析，发现是搜索电影
#   先向https://www.dygod.net/e/search/index.php发送一个post请求，然后返回一个302重定向链接，再重定向到对应的网址，该POST请求的参数可以在
#   data中查看到，但是"keyboard"无法解码，从网址中看到该网址编码为gb2312，分析可能是进行了该编码，因此尝试发送请求。
#3. 得到该链接后，需要获取到下载链接
#################################
'''
# class get_movie_url():
#     lock = threading.Lock()
#     def get_headers(self):
#         user_agent_list = [
#         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
#         'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
#         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6']
#         UA = random.choice(user_agent_list)
#         headers = {'User-Agent': UA}
#         return headers
#     def get_movie(self,s):#获取搜索到的电影名称，和跳转的地址
#         s = s.encode("gb2312")
#         print(s)
#         url = "https://www.dygod.net/e/search/index.php"
#         data = {"show": "title",
#                 "tempid": "1",
#                 "keyboard": s}
#         headers = self.get_headers()
#         print(headers)
#         movie_urls = {}
#         try:
#             rsp = requests.post(url=url, data=data, headers=headers).text
#             soup = BeautifulSoup(rsp,"lxml")
#             soup = soup.find_all("a",{"class":"ulink"})
#             for i in soup:
#                 movie_name = i["title"]
#                 movie_url = "https://www.dygod.net/" + i["href"]
#                 movie_urls.update({movie_name:movie_url})
#         except requests.exceptions as e:
#             print(e)
#         return movie_urls
#
#     def get_url(self,url): #获取电影最终的下载链接
#         print(url)
#         headers = self.get_headers()
#         try:
#             rsp = requests.get(url=url,headers=headers).text.encode("ISO-8859-1").decode("gbk",errors='ignore') #可以利用rsp.encoding方法查看返回的编码格式，然后编码再解码
#             # print(rsp)
#             soup = BeautifulSoup(rsp,"lxml")
#             soup = soup.find("td",{"style":"WORD-WRAP: break-word","bgcolor":"#fdfddf"})
#             print("-------",soup.a["href"])
#         except EXCEPTION as e:
#             print(e)
#             return None
#         return soup.a["href"]
#
#     def get_final(self,list_queue): #获取最终的名字和下载链接
#         if not list_queue.empty():
#             print("准备获取最终电影链接")
#             (movie,url), = list_queue.get().items()
#             finanl_url = self.get_url(url)
#             final.update({movie:finanl_url})
#             print(final)
#         # else:
#         #     showinfo("提示","未搜索到此电影")
#         #     return {}
#
#         '''
#         if movie_urls:
#             # final = {}
#             for k,v in movie_urls.items():
#                 u = self.get_url(v)
#                 # mlb.insert(END, (k, u))
#                 final.update({k:u})
#             # return final
#             print(final)
#         else:
#             showinfo("提示","未搜索到此电影")
#             return {}
#         '''

'''  
#该部分是使用tkinter实现，效果一般
#Tkinter实现Listbox控件单行多值
#此处是为了构造多列的显示表框
class MultiListbox(Frame):
    def __init__(self,master,lists):
        Frame.__init__(self,master)
        self.lists = []
        for l, w in lists:
            frame = Frame(self)
            frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0, relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind("<B1-Motion>",lambda e, s=self: s._select(e.y))
            lb.bind("<Button-1>",lambda e,s=self: s._select(e.y))
            lb.bind("<Leave>",lambda e: "break")
            lb.bind("<B2-Motion>",lambda e,s=self: s._b2motion(e.x,e.y))
            lb.bind("<Button-2>",lambda e,s=self: s._button2(e.x,e.y))
        frame = Frame(self)
        frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame,orient=VERTICAL, command=self._scroll)
        sb.pack(side=LEFT, fill=Y)
        self.lists[0]["yscrollcommand"] = sb.set
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return "break"
    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x,y)
        return "break"
    def _b2motion(self, x, y):
        for l in self.lists:
            l.scan_dragto(x, y)
        return "break"
    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)
        return "break"
    def curselection(self):
        return self.lists[0].curselection()
    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first,last)
    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last:
            return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0],index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1
    def size(self):
        return self.lists[0].size()
    def see(self, index):
        for l in self.lists:
            l.see(index)
    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)
    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first,last)
    def selection_includes(self, index):
        return self.lists[0].seleciton_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

def button_click():

    list_queue = Queue()
    input_name = edit.get()
    a = get_movie_url()
    lst = a.get_movie(input_name)
    print(lst)
    for k,v in lst.items():
        list_queue.put({k:v})
    thread_list=[]
    for i in range(list_queue.qsize()):
        jincheng = threading.Thread(target = a.get_final,args=(list_queue,))
        print("------第{}进程-------".format(i))
        jincheng.start()
        thread_list.append(jincheng)
    for jincheng in thread_list:
        jincheng.join()
    for k, v in final.items():
        mlb.insert(END, (k, v))

    # if c:
    #     print(c)
    #     for k,v in c.items():
    #         mlb.insert(END, (k,v))
    # else:
    #     pass

#这部分是为了可视化，使用TKinter，这里先屏蔽掉，后续使用pyqt来实现
final = {}
review = Tk()
review.title("电影爬取")
review.geometry('850x400')
label1 = Label(review,text="搜索框：",height=1)
edit = Entry(review,width=30)
mlb = MultiListbox(review,(('Subject', 30),('Sender', 50)))
bontton = Button(review,text="搜索电影",command=button_click)
label1.place(x=50,y=20)
edit.place(x=150, y=20)
mlb.place(x=50, y=60)
bontton.place(x=450,y=15)
review.mainloop()


# a = get_movie_url()
# s = a.get_movie("你的名字")
# a.get_final(s)
'''
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
        list_queue = Queue()
        thread_list = []
        global final
        final = {}
        movie_name = self.Edit.text()
        a = sekf.get_movie(movie_name)
        for k, v in a.items():
            list_queue.put({k: v})
        for i in range(list_queue.qsize()):
            jincheng = threading.Thread(target=self.get_final, args=(list_queue,))
            print("------第{}进程-------".format(i))
            jincheng.start()
            thread_list.append(jincheng)
        for jincheng in thread_list:
            jincheng.join()
        for k, v in final.items():
            self.model.appendRow(QStandardItem([k,v])

    # def processtrigger(self,action):
    #     if action.text()=="添加":
    #         self.model.appendRow([
    #             QStandardItem('row %s,column %s' % (11, 11)),
    #             QStandardItem('row %s,column %s' % (11, 11)),
    #             QStandardItem('row %s,column %s' % (11, 11)),
    #             QStandardItem('row %s,column %s' % (11, 11)),
    #         ])
    #     if action.text()=="删除":
    #
    #         r= self.tableView.selectionModel().selectedRows()#获取被选中行
    #         print(r)#被选中行的列表，每个元素是ModelIndex对象
    #         #indexs = self.tableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
    #         #print(indexs[0].row())
    #         if r:
    #             #下面删除时，选中多行中的最后一行，会被删掉；不选中，则默认第一行删掉
    #             index=self.tableView.currentIndex()
    #             print(index.row())
    #             self.model.removeRow(index.row())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())