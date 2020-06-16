import pdfkit 
from bs4 import BeautifulSoup
import requests
import sys
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QComboBox, QVBoxLayout, QLineEdit ,QTextEdit, QSystemTrayIcon,QMenu,QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from urllib.parse import urljoin


combo_options = ["Smart search - by next button text","By <a> tag class", "By <a> tag container class"]

class web2pdf(object):
    def __init__(self):
        self.url = None
        self.search_by = None
        self.nxtBtnTxt = None
        self.elem_class = None
        self.depth = 0
        self.file_path = "./result/"
        self.file_prefix = "Page"

    def savePDF(self,url, fname):
        pdfkit.from_url(url,fname)
        status.append("from url: "+url+" ===>  saving... ->"+fname)

    def getNextLinks(self):
        if(self.search_by == 0):
            if(self.nxtBtnTxt == None):
                status.append("button text required")
                return []
            return self.smartFindNextLink()
        elif(self.search_by == 1):
            if(self.elem_class == None):
                status.append("<a> tag class required")
                return []
            return self.getNextLinksWithAClass()
        elif(self.search_by == 2):
            if(self.elem_class == None):
                status.append("<a> tag wrapper element class required")
                return []
            return self.getNextLinksWithContainerClass()
            

    def getBaseUrl(self,href):
        return urljoin(self.url, href)

    def webtopdf(self):
        #-------- Get the links based on  criteria --------------
        # get the links
        links = self.getNextLinks()
        print(links)
        if(not links):
            submit_btn.setEnabled(True)
            return
        #save pdf from links
        for idx,link in enumerate(links):
            self.savePDF(link, self.file_path+self.file_prefix+str(idx+1)+".pdf")
        submit_btn.setEnabled(True)

    # need to make this function dynamic to fit various search criteria-----------------------------------
    def getNextLinksWithContainerClass(self):
        links =[]
        links.append(self.url)
        start_url = self.url
        for i in range(self.depth-1):
            try:
                page = requests.get(start_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                nextPage = soup.find(class_=self.elem_class)
                link = nextPage.find('a')
                nxt_link = self.getBaseUrl(link['href'])
                links.append(nxt_link)
                start_url = nxt_link
            except:
                status.append("error making request to"+ start_url)
        return links

    def getNextLinksWithAClass(self):
        links =[]
        links.append(self.url)
        start_url = self.url
        for i in range(self.depth-1):
            try:
                page = requests.get(start_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                nextPage = soup.findAll('a',{"class":self.elem_class})
                print(nextPage)
                nxt_link = self.getBaseUrl(nextPage[0]['href'])
                links.append(nxt_link)
                start_url = nxt_link
            except:
                status.append("error making request to" + start_url)
        return links

    
    def smartFindNextLink(self):
        links =[]
        links.append(self.url)
        start_url = self.url
        for i in range(self.depth):
            page = requests.get(start_url)
            soup = BeautifulSoup(page.content,'html.parser')
            next_url = start_url
            for link in soup.findAll('a' ,{'href':True}):
                if(link.text.strip() == self.nxtBtnTxt):
                    next_url = self.getBaseUrl(link['href'])
                    links.append(next_url)
            start_url=next_url
        return links

if __name__ == "__main__":
    w2p = web2pdf()
    def setw2pData():
        # checcking and setting
       
        w2p.url = page_url.text()
        w2p.search_by = search_by.currentIndex()

        if(page_url.text()==""):
            status.append("url is required")
            return -1

        if(w2p.search_by==0 and search_inp.text()!=""): w2p.nxtBtnTxt = search_inp.text()
        else:
            if(search_inp.text()!=""): w2p.elem_class = search_inp.text()
        
        if(depth.text().isnumeric()):w2p.depth = int (depth.text())
        else:
            status.append("invalid number of pages")
            return -1
        
        if(abs_path.text()!=""): w2p.file_path = abs_path.text()
        if(file_prefix.text()!=""): w2p.file_prefix = file_prefix.text()

    def makePDFBaby():
        status.setText("")
        if(setw2pData()==-1): return 
        def run():
            try:
                w2p.webtopdf()
            except KeyboardInterrupt:
                print("Press Ctrl-C to terminate while statement")
                pass

        thread = threading.Thread(target=run)
        thread.setDaemon(True)
        thread.setName("make pdf thread")
        thread.start()
        submit_btn.setDisabled(True)
        pass


    # main window
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Web2PDF')
    #window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # main -layout
    layout = QVBoxLayout()


    # all lables
    page_url_label = QLabel("Full Url")
    search_by_label = QLabel("Search by")
    search_inp_label = QLabel("Class or Btn text")
    depth_label = QLabel("Number of pages")
    abs_path_label = QLabel("Save to")
    file_prefix_label = QLabel("File prefix (default Page)")

    # full_url
    page_url = QLineEdit()
    page_url.setPlaceholderText("Page Url")

    # combo box
    search_by = QComboBox()
    search_by.addItems(combo_options)
    
    
    # combo box linked val
    search_inp = QLineEdit()
    search_inp.setPlaceholderText("search class or tag or attr")
    

    # depth
    depth = QLineEdit()
    depth.setPlaceholderText("Num of pages eg 5")
    

    # abs_file_path
    abs_path = QLineEdit()
    
    abs_path.setPlaceholderText("abs url to file where to save pdf")

    # file_prefix
    file_prefix = QLineEdit()
    file_prefix.setPlaceholderText("File prefix")
    

    # submit button
    submit_btn = QPushButton("Submit")
    submit_btn.clicked.connect(makePDFBaby)

    # status text
    status = QTextEdit()
    status.setReadOnly(True)
    
    # add everything to layout
    layout.addWidget(page_url_label)
    layout.addWidget(page_url)
    layout.addWidget(search_by_label)
    layout.addWidget(search_by)
    layout.addWidget(search_inp_label)
    layout.addWidget(search_inp)
    layout.addWidget(depth_label)
    layout.addWidget(depth)
    layout.addWidget(abs_path_label)
    layout.addWidget(abs_path)
    layout.addWidget(file_prefix_label)
    layout.addWidget(file_prefix)

    layout.addWidget(submit_btn)
    layout.addWidget(status)
   
    
    window.setLayout(layout)
    window.setFixedSize(350,600)
    window.show()
    sys.exit(app.exec_())