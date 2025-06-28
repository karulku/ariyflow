from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QTextEdit,QMessageBox

"""
    QPushButton:
    pyQt中的事件绑定和tkinter不同，需要使用QPushButton中的属性clicked的函数connect来绑定，比如：
btn01.clicked.connect(btn_event01)
    clicked可以看作是一个信号（signal），当btn01发出这个信号时，就会调用它所绑定的事件处理函数（slot）
    可以类比为linux中的信号和信号处理函数signal/signal_handler，理解起来方便一点
    
    QTextEdit:
    获取当前输入的文本的函数：
        toPlainText()
"""

"""
    信息表：
薛蟠 4560 25
薛蝌 4460 25
薛宝钗 35776 23
薛宝琴 14346 18
王夫人 43360 45
王熙凤 24460 25
王子腾 55660 45
王仁 15034 65
尤二姐 5324 24
贾芹 5663 25
贾兰 13443 35
贾芸 4522 25
尤三姐 5905 22
贾珍 54603 35
"""

def btn_event01():
    print("you clicked!")
    text = text01.toPlainText() # 获取目前输入的文本
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
        
        QMessageBox.about(window,"提示",f"统计信息：\n薪资20000及以上的有：{','.join(upper)}\n薪资20000以下的有：{','.join(lower)}")
    else:
        QMessageBox.warning(window,"提示","请正确输入内容！")

app = QApplication()

window = QMainWindow()
window.setWindowTitle("按钮事件的处理")
window.resize(500,400)
window.move(300,300)

text01 = QTextEdit(window)
text01.resize(200,300)
text01.move(10,10)
text01.setPlaceholderText("请输入内容")

btn01 = QPushButton("click",window)
btn01.move(220,10)
btn01.clicked.connect(btn_event01) # 为btn01绑定事件

window.show()

app.exec()