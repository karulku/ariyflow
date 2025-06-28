from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QTextEdit,QMessageBox

"""
    GUI封装是非常必要的一个步骤，所以需要对代码做好封装，这个过程和tkinter基本一致
"""

class APP():
    def __init__(self):
        self.window = QMainWindow()
        self.window.setWindowTitle("按钮事件的处理")
        self.window.resize(500,400)
        self.window.move(300,300)
        
        self.createWidgets()
    
    def createWidgets(self):
        self.text01 = QTextEdit(self.window)
        self.text01.resize(200,300)
        self.text01.move(10,10)
        self.text01.setPlaceholderText("请输入内容")

        self.btn01 = QPushButton("click",self.window)
        self.btn01.move(220,10)
        self.btn01.clicked.connect(self.btn_event01) # 为btn01绑定事件

    def btn_event01(self):
        print("you clicked!")
        text = self.text01.toPlainText() # 获取目前输入的文本
        if text:
            lines = text.split("\n")
            upper = []
            lower = []
            for line in lines:
                info = line.split(" ")
                k = info[0]
                v = info[1]
                if int(v) >= 20000:
                    upper.append(k)
                else:
                    lower.append(k)
        
            QMessageBox.about(self.window,"提示",f"统计信息：\n薪资20000及以上的有：{','.join(upper)}\n薪资20000以下的有：{','.join(lower)}")
        else:
            QMessageBox.warning(self.window,"提示","请正确输入内容！")

if __name__ == "__main__":
    app = QApplication()
    win = APP()
    win.window.show()
    app.exec()