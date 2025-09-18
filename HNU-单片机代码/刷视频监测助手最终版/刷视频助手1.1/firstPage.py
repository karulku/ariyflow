from PySide6.QtWidgets import (
    QWidget, QMainWindow, QPushButton, QPlainTextEdit,QMessageBox
)

class firstPage(QWidget):
    def __init__(self, par):
        super().__init__()
        self.par = par
        self.page = self.par.findChild(QWidget, "first_page")
        self.cookie = ""

        self.load_widgets()
        self.bind_events()
    
    def load_widgets(self):
        self.add_cookie_btn = self.page.findChild(QPushButton,"add_cookie_btn") # type: ignore
        self.open_bilibili_btn = self.page.findChild(QPushButton,"open_bilibili_btn") # type: ignore
        self.cookie_text = self.page.findChild(QPlainTextEdit,"cookie_text") # type: ignore
    
    def bind_events(self):
        self.add_cookie_btn.clicked.connect(self.add_cookie_event) # type: ignore
        self.open_bilibili_btn.clicked.connect(self.open_bilibili_event) # type: ignore
    
    def add_cookie_event(self):
        tmp = self.cookie_text.toPlainText() # type: ignore
        if tmp:
            self.cookie = tmp.strip()
            if self.par.bilibiliThread:
                self.par.bilibiliThread.add_cookie(self.cookie)
                print("添加cookie成功")
            else:
                print("添加cookie失败")
        else:
            QMessageBox.warning(None,"提示","请输入有效内容！")
    
    def open_bilibili_event(self):
        self.par.bilibiliThread.open_bilibili()
    
    def execute_instruction(self, instruction):
        pass