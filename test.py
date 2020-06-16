import pdfkit 
from bs4 import BeautifulSoup
import requests
import sys
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QComboBox, QVBoxLayout, QLineEdit ,QTextEdit, QSystemTrayIcon,QMenu,QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from urllib.parse import urljoin


url ="https://www.w3schools.com/python/python_intro.asp"
href="python_getstarted.asp"

def getBaseUrl(url):
    li = url.split("/")
    print(li[0]+"//"+li[2])

def smartFindNextLink(url):
    nxtBtnTxt= "Next ❯"
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    for link in soup.findAll('a' ,{'href':True}):
        if(link.text.strip() == nxtBtnTxt):
            print(link['href'])
       

print(urljoin(url, href))