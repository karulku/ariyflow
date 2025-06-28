# tkinter暂时告一段落，下面准备学pyQt了，毕竟tkinter能做的事情太少了
# 使用的包：pySide6
from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit
"""
QtWidgets: qt的组件库，后面会慢慢学习
QApplication: 应用底层管理，所有Qt程序都要创建
                exec(): 程序的主循环，类似mainloop，保证UI一直显示
QMainWindow: 创建一个主窗口界面，这里还没有显示，只是创建
                resize(width,height) 设置大小
                move(width,height) 布局位置，这两个函数的功能类似tkinter中Tk类的geometry
                setWindowTitle("example") 设置标题，类似tkinter中Tk类的title函数
                show() 展示界面，一般调用最上层的组件展示
QPlainTextEdit: 纯文本框
                setPlaceholderText("example") 没有内容时的提示文本
                move(width,height) 布局，相对于父容器的位置，类似place布局管理器
                resize(width,height) 设置大小
QPushButton: 按钮组件

"""

app = QApplication() # 创建app

window = QMainWindow() # 创建主窗口
window.resize(500,400) # 设置大小
window.move(300,310) # 设置位置，这里是相对于电脑屏幕
window.setWindowTitle("test01") # 设置标题

textEdit = QPlainTextEdit(window) # 文本框
textEdit.setPlaceholderText("请输入内容") # 未输入文本时默认显示的内容
textEdit.move(10,10) # 位置，这里是相对父容器
textEdit.resize(300,350)

btn01 = QPushButton("统计",window) # 这里注意QT的button声明是先text再父容器
btn01.move(320,10)

window.show()

app.exec()