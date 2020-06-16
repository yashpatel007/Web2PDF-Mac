import pdfkit 
from bs4 import BeautifulSoup
import requests
import sys
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QComboBox, QVBoxLayout, QLineEdit ,QTextEdit, QSystemTrayIcon,QMenu,QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

def savePDF(url, fname):
    pdfkit.from_url(url,fname)
    status.append("from "+url+"  saving... "+fname)
    
def getNextLinks(start_url, depth,elem_class):
    links =[]
    for i in range(depth):
        page = requests.get(start_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        nextPage = soup.find(class_=elem_class)
        link = nextPage.find('a')
        nxt_link = getBaseUrl(start_url)+link['href']
        links.append(nxt_link)
        start_url = nxt_link
    return links

def webtopdf(full_url,depth, elem_class):
    links = getNextLinks(full_url,int(depth), elem_class)
    for idx,link in enumerate(links):
        savePDF(link, "page"+str(idx)+".pdf")
    submit_btn.setEnabled(True)

def getBaseUrl(url):
    li = url.split("/")
    return li[0]+"//"+li[2]


if __name__ == "__main__":
   
    def makePDFBaby():
        mpb_url = str(page_url.text())
        mpb_depth = int(depth.text())
        mpb_tag = str(search_inp.text())
        #status.append(mpb_url+"/n"+mpb_tag+"/n"+str(mpb_depth))
        def run():
            try:
                webtopdf(mpb_url,mpb_depth,mpb_tag)
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

    #base url
    page_url = QLineEdit()
    page_url.setFixedWidth(350)
    page_url.setPlaceholderText("Page Url")

    search_by = QComboBox()
    search_by.addItems(['class','tag','attribute'])
    search_by.setFixedWidth(350)
    
    search_inp = QLineEdit()
    search_inp.setPlaceholderText("search class or tag or attr")
    search_inp.setFixedWidth(350)

    depth = QLineEdit()
    depth.setPlaceholderText("Num of pages eg 5")
    depth.setFixedWidth(350)

    abs_path = QLineEdit()
    abs_path.setFixedWidth(350)
    abs_path.setPlaceholderText("abs url to file where to save pdf")

    submit_btn = QPushButton("Submit")
    submit_btn.clicked.connect(makePDFBaby)

    status = QTextEdit()
    status.setReadOnly(True)
    
    layout.addWidget(page_url)
    layout.addWidget(search_by)
    layout.addWidget(search_inp)
    layout.addWidget(depth)
    layout.addWidget(abs_path)
    layout.addWidget(submit_btn)
    layout.addWidget(status)
   
    
    window.setLayout(layout)
    window.setFixedSize(400,300)
    window.show()
    sys.exit(app.exec_())
