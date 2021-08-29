import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic
from bs4 import BeautifulSoup

form_class = uic.loadUiType("C:\\tistory_project\\blog_auto_writing.ui")[0]

class WindowClass(QMainWindow, form_class) :
    access_token = ''
    blog_name = ''
    problem_number = 0
    message = ''

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_enter.clicked.connect(self.upload)
        self.btn_reset.clicked.connect(self.clear)
        self.btn_save.clicked.connect(self.save)
        self.btn_load.clicked.connect(self.load)

    def printResult(self, string) :
        message = QLabel(WindowClass.message + '\n' + string)
        self.result_scroll.setWidget(message)
        WindowClass.message += '\n' + string
    
    def clear(self) :
        self.edit1.clear()
        self.edit2.clear()
        self.edit3.clear()
        self.printResult('[-] Reset!')

    def getInfo(self) :
        WindowClass.access_token = self.edit1.text()
        WindowClass.blog_name = self.edit2.text()
        WindowClass.problem_number = self.edit3.text()
    
    def getData(self) :
        boj_url = 'https://www.acmicpc.net/problem/' + WindowClass.problem_number
        response = requests.get(boj_url)
    
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select_one('#problem_title').get_text()
            
        print(data)
        return data

    def getTitle(self, problem_title) :
        title = '백준 ' + self.problem_number + '번: ' + problem_title
        return title

    def getContent(self) :
        content = '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16"><b>0. 알고리즘 분류</b></p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16"><b>1. 문제</b></p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16"><b>2. 풀이</b></p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        content += '<p data-ke-size="size16"><b>3. 코드</b></p>'
        content += '<p data-ke-size="size16">&nbsp;</p>'
        return content

    def post(self, content, title) :
        tistory_url = 'https://www.tistory.com/apis/post/write?'
        parameters = {
            'access_token' : WindowClass.access_token,
            'output' : 'txt',
            'blogName' : WindowClass.blog_name,
            'title' : title,
            'content' : content,
            'visibility' : '3',
            'category' : '979110',
            'tag' : '백준, BOJ'
        }
        result = requests.post(tistory_url, params=parameters)
        if result.status_code == 200 :
            self.printResult('[-] Upload Success!\n' + result.url)
        else :
            self.printResult('[!] Failed! ' + result.status_code)
        

    def upload(self) :
        self.getInfo()
        self.getData()
        self.post(self.getContent(), self.getTitle(self.getData()))

    def save(self) :
        if self.edit1.text() == '' or self.edit2.text() == '':
            self.printResult('[!] Fill in blanks!')
            return

        f = open("info.txt", 'w')
        data = self.edit1.text() + '\n' + self.edit2.text() + '\n'
        f.write(data)
        f.close()
        self.printResult('[-] Data was saved!')

    def load(self) :
        f = open("info.txt", 'r')
        data = f.readlines()
        self.edit1.setText(data[0].strip())
        self.edit2.setText(data[1].strip())
        f.close()
        self.printResult('[-] Data Was Loaded!')
        

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = WindowClass() 

    myWindow.show()

    app.exec_()