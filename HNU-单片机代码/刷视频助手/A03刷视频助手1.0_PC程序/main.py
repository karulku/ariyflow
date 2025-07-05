from PySide6.QtWidgets import (
    QApplication,QMainWindow,QPushButton,QLineEdit,QPlainTextEdit,
    QComboBox,QTabWidget,QWidget,QFrame,QGroupBox,QMessageBox,
    QFileDialog)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile,QThread,Signal,QMutex
import serial
from time import sleep
from threading import Event
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

"""
数据传输规则：
    每个数据包一共8个字节，形式为：10 29 xx xx xx xx xx xx
    前两个字节为数据包头，固定为10 29，后六个字节为传输的数据
    第2个字节为选择的模式，目前的设计有三种模式：
    00 -- 刷视频助手
    01 -- 实时时钟
    02 -- 温光检测

00 -- 刷视频助手
    第3个字节为指令
        00 -- 刷新页面
        ff -- 退出视频（如果打开了视频，没有打开视频会直接退出）
        01 -- 点开第1个视频 02 -- 点开第2个视频 03 -- 点开第2个视频
        04 -- 点开第4个视频 05 -- 点开第5个视频 06 -- 点开第6个视频
        fe -- 直接退出，不管是否打开视频
        # 除此以外，在单片机程序中还要加上导航中间的逻辑，按下后数值重置为0
    第4个字节为前置指令（不是对bilibiliThread内部的操作）
        如果为00，那么会正常执行前面第3个字节对应的操作
        如果不为00，第3个字节无效，这条指令不会在bilibiliThread中处理，转为在firstPage中处理，处理结束后指令重置
            01 -- 打开b站   (10 29 00 xx 01 xx xx) 
    
01 -- 实时时钟
"""

# 主窗口
class APPWindow(QMainWindow):
    def __init__(self, app:QApplication):
        super().__init__()
        self.win = QUiLoader().load(QFile("./A03.ui"))
        self.setCentralWidget(self.win)
        self.setWindowTitle("测试程序1.0")
        self.setGeometry(300,200,1080,720)
        
        self.app = app
        self.app.aboutToQuit.connect(self.quitAppEvent) # 在退出时调用quitApp函数
        
        self.tabWidget = self.win.findChild(QTabWidget,"tabWidget") # tab标签
        self.currentTabIndex = self.tabWidget.currentIndex() # 变量记录当前标签页的索引
        self.tabWidget.currentChanged.connect(self.tabChangedEvent)
        
        self.first_page = firstPage(self.tabWidget.findChild(QWidget,"first_page"), self) # 第一个页面 -- 刷视频助手，所有对第一个页面的操作都封装到firstPage中

    # 标签页切换的事件
    def tabChangedEvent(self, index):
        # 目前只做了一个页面，所以暂时没用
        if self.currentTabIndex == 0:
            print(f"原先标签页：{self.tabWidget.tabText(self.currentTabIndex)}")
        elif self.currentTabIndex == 1:
            print(f"原先标签页：{self.tabWidget.tabText(self.currentTabIndex)}")
        elif self.currentTabIndex == 2:
            print(f"原先标签页：{self.tabWidget.tabText(self.currentTabIndex)}")
        
        self.currentTabIndex = index
    
    # 退出程序
    def quitAppEvent(self):
        # 如果tab1的串口没有关闭，自动关闭串口
        if self.first_page.ser and self.first_page.ser.is_open:
            self.first_page.serialRunning.clear()
            self.first_page.ser.close()
            QMessageBox.about(self.win,"提示","串口未关闭，已自动关闭！")
        if self.first_page.bilibiliRunning.is_set():
            self.first_page.bilibiliRunning.clear()
            self.first_page.bilibiliThread.wait()
            
            
# 第一个页面 -- 刷视频助手
class firstPage(QWidget):
    
    uartData = b"" # 用于不同线程间的通信
    mut = QMutex() # 访问data的锁
    bilibiliRunning = Event()
    
    def __init__(self,page:QWidget, parentWin:APPWindow):
        super().__init__()
        self.page = page # page页面是tab1
        self.parentWin = parentWin # parentWin是APPWindow
        self.ser = serial.Serial() # 串口通信
        self.cookie = "" # 保存输入的cookie
        self.frame = self.page.findChild(QFrame,"frame") # tab1的frame
        self.loadWidget()
        self.bindBtnEvent()
        
        try:
            self.ser.port = self.serial_name.text()
            self.ser.baudrate = int(self.baudrate_select.currentText())
            self.ser.timeout = float(self.delay_time.currentText()[:-1])
            self.ser.open()
            
            self.serialRunning = Event() # serial线程运行的标志位
            self.serialRunning.set()
            self.serialThread = SerialThread(self.ser,self)
            self.serialThread.dataPipe.connect(self.setUartData)
            self.serialThread.log.connect(self.tprint)
            self.serialThread.start()
            
            self.tprint(f"自动打开串口成功")
        except:
            self.tprint("自动打开串口失败，请正确设置参数并手动打开")
    
    def loadWidget(self):
        self.setting_layout = self.frame.findChild(QGroupBox,"setting_groupBox") # 设置栏
        
        self.baudrate_select = self.setting_layout.findChild(QComboBox,"baudrate_select")
        self.serial_name = self.setting_layout.findChild(QLineEdit,"serial_name")
        self.delay_time = self.setting_layout.findChild(QComboBox,"delay_time")
        self.open_serial_btn = self.setting_layout.findChild(QPushButton,"open_serial_btn")
        self.close_serial_btn = self.setting_layout.findChild(QPushButton,"close_serial_btn")
        self.exit_app_btn = self.setting_layout.findChild(QPushButton,"exit_app_btn")
        self.add_cookie_btn = self.setting_layout.findChild(QPushButton,"add_cookie_btn")
        self.open_bilibili_btn = self.setting_layout.findChild(QPushButton,"open_bilibili_btn")
        self.cookie_text = self.setting_layout.findChild(QPlainTextEdit,"cookie_text")
        
        self.log_groupBox = self.frame.findChild(QGroupBox,"log_groupBox") # 日志栏
        
        self.clear_log_btn = self.log_groupBox.findChild(QPushButton,"clear_log_btn")
        self.save_log_btn = self.log_groupBox.findChild(QPushButton,"save_log_btn")
        self.message_text = self.log_groupBox.findChild(QPlainTextEdit,"message_text")
    
    def bindBtnEvent(self):
        self.open_serial_btn.clicked.connect(self.open_serial_event)
        self.close_serial_btn.clicked.connect(self.close_serial_event)
        self.exit_app_btn.clicked.connect(self.exit_app_event)
        self.add_cookie_btn.clicked.connect(self.add_cookie_event)
        self.open_bilibili_btn.clicked.connect(self.open_bilibili_event)
        self.clear_log_btn.clicked.connect(self.clear_log_event)
        self.save_log_btn.clicked.connect(self.save_log_event)
    
    # 打开串口事件
    def open_serial_event(self):
        if self.ser.is_open:
            QMessageBox.warning(self.frame,"提示","串口已打开！")
            return 0
        try:
            self.ser.port = self.serial_name.text()
            self.ser.baudrate = int(self.baudrate_select.currentText())
            self.ser.timeout = float(self.delay_time.currentText()[:-1])
            # print(float(self.delay_time.currentText()[:-1]))
            self.ser.open()
        except:
            QMessageBox.warning(self.frame,"提示","串口打开失败，请检查参数设置或串口连接！")
            return -1
        
        # 此处需要添加串口线程
        self.serialRunning = Event() # serial线程运行的标志位
        self.serialRunning.set()
        self.serialThread = SerialThread(self.ser,self)
        self.serialThread.dataPipe.connect(self.setUartData)
        self.serialThread.log.connect(self.tprint)
        self.serialThread.start()
    
    # 关闭串口事件
    def close_serial_event(self):
        if not self.ser.is_open:
            QMessageBox.warning(self.frame,"提示","串口未打开！")
            return
        
        self.serialRunning.clear()
        self.ser.close()
        self.tprint("串口已关闭")
    
    # 退出程序事件
    def exit_app_event(self):
        self.parentWin.quitAppEvent()
        self.parentWin.app.quit()
    
    # 添加cookie事件
    def add_cookie_event(self):
        tmp = self.cookie_text.toPlainText()
        if tmp:
            self.cookie = tmp.strip()
        else:
            QMessageBox.warning(self.frame,"提示","请输入有效内容！")
    
    # 打开b站事件
    def open_bilibili_event(self):
        
        self.bilibiliRunning.set()
        self.bilibiliThread = BilibiliThread(self)
        self.bilibiliThread.log.connect(self.tprint)
        self.bilibiliThread.start()
    
    # 清空日志事件
    def clear_log_event(self):
        select = QMessageBox.question(self.frame,"提示","确认清空日志？",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if select == QMessageBox.StandardButton.Yes:
            self.message_text.clear()
    
    # 保存日志事件
    def save_log_event(self):
        try:
            location = QFileDialog.getExistingDirectory(self,"日志保存位置")
            if location != "":
                now_time = datetime.now()
                file_name = f"firstPage_log_{now_time.year}_{now_time.month}_{now_time.day}_{now_time.hour}_{now_time.minute}_{now_time.second}"
                with open(f"{location}/{file_name}.log",mode="w",encoding="utf-8") as file:
                    file.write(self.message_text.toPlainText().strip())
                QMessageBox.about(None,"提示",f"日志成功保存到：\n{location}/{file_name}.log")
        except Exception as e:
            QMessageBox.warning(None,"提示","未知错误，日志保存失败！")
    
    # 输出日志函数，将日志信息输出到日志栏的QPlainText
    def tprint(self,msg:str):
        self.message_text.appendPlainText(msg)
    
    # 添加设置数据和获取数据的函数，用于信息交互
    def setUartData(self,data:bytes):
        """ 将uartData设置为新值，并返回旧值 """
        self.mut.lock()
        tmp = self.uartData
        self.uartData = data
        if self.uartData: # 如果收到一个不为空的数据包
            self.tprint(f"收到数据包：{[bit.to_bytes().hex() for bit in self.uartData]}")
            self.uartDataParse() # 在设置完后对data进行解析，看是否为前置指令，要放在锁里面
        self.mut.unlock()
        # print(f"uartData已被设置为：{self.uartData}")
        return tmp

    def getUartData(self):
        return self.uartData

    def uartDataParse(self):
        # 由于这个函数只在setUartData中调用，而这个函数是持有锁的，所以可以放心对共享变量uartData操作
        data = self.uartData
        if data[0] == 0x10 and data[1] == 0x29: # 数据包符合规范，其实都不用判断的，设置之前就会判断包头
            
            if data[2] == 0x00 and data[4] != 0x00: # 模式1： 刷视频助手
                self.tprint(f"该指令为[00]的前置指令，指令码：{data[4].to_bytes().hex()}")
                if data[4] == 0x01: # 打开b站的操作，触发打开b站事件
                    self.uartData = b"" # 这里不能调用setUartData清除，会发生死锁，直接赋值清除即可
                    self.open_bilibili_event()
                elif data[4] == 0x02: # 关闭串口事件
                    self.close_serial_event()
                else:
                    self.tprint(f"操作[{data[4].to_bytes().hex()}]未定义，指令无效！")

# 只能由firstPage操作的串口线程
class SerialThread(QThread):
    dataPipe = Signal(bytes)
    log = Signal(str)
    
    def __init__(self,ser:serial.Serial,parent:firstPage):
        super().__init__()
        self.par = parent
        self.ser = ser
        
    
    # QThread必须实现这一个函数，在对象调用start后，run函数会运行
    def run(self):
        reading = b""
        self.log.emit("线程 Serial 开始运行")
        while self.par.serialRunning.is_set():
            reading = self.ser.read(8) # 这里把包头设置为8个字节，后面可能没法修改了
            if reading:
                if reading[0:2] == b"\x10\x29" and len(reading) == 8:
                    self.dataPipe.emit(reading)
                elif reading[0:2] != b"\x10\x29":
                    self.log.emit(f"收到数据包，但是包头错误：{reading.hex()}")
                elif len(reading) != 8:
                    self.log.emit(f"收到数据包，但是字节数错误：{reading.hex()}")
            else:
                self.log.emit("未收到数据包，继续轮询...")
        
        self.log.emit("线程 Serial 准备退出")
        return 0

# 只能由firstPage操作的bilibili线程
class BilibiliThread(QThread):
    log = Signal(str)
    def __init__(self,par:firstPage):
        super().__init__()
        self.par = par
        self.web = webdriver.Edge()
        self.url = "https://www.bilibili.com"
        self.cookie = self.par.cookie
        if not self.cookie:
            self.cookie = "" # 如果没有输入cookie，会使用这里放的cookie，我自己测试程序的时候用的，所以上传github时会删除
    def run(self):
        self.log.emit("bilibiliThread 开始运行")
        self.web.get(self.url)
        self.web.maximize_window()
        
        cookie_list = []
        msg_list = self.cookie.split("; ")
        for msg in msg_list:
            k,v = msg.split("=")
            cookie_list.append({"name":k.strip(),"value":v.strip(),"domain":".bilibili.com"})
        
        for cookie in cookie_list:
            self.web.add_cookie(cookie)
        
        self.web.refresh()
        self.log.emit("bilibiliThread 准备完毕")
        self.par.setUartData(b"") # 这里需要把数据缓冲区原先的内容清零，否则会影响后面的逻辑
        
        # 此处需要添加收到数据包后的处理逻辑
        while self.par.bilibiliRunning.is_set():
            self.par.mut.lock()
            data = self.par.getUartData()
            self.par.mut.unlock()
            self.par.setUartData(b"") # 每次获取到数据后将缓冲区清空
            if data:
                self.log.emit(f"bilibiliThread收到数据：{[bit.to_bytes().hex() for bit in data]}")
                if data[0] == 0x10 and data[1] == 0x29 and data[2] == 0x00:
                    """ 只有包头正确并且第2个字节的模式设置正确才会进入bilibiliThread的处理逻辑 """
                    com = data[3]
                    self.log.emit(f"提取到指令：{com.to_bytes().hex()}")
                    if com == 0x00: # 刷新页面
                        self.web.find_element(By.XPATH,"//button[@class='primary-btn roll-btn']").click()
                    elif com <= 6 and com >= 1: # 打开视频（如果有的话）
                        video_list = self.web.find_elements(By.XPATH,"//div[@class='feed-card']")
                        try:
                            video_list[int(com)].click()
                            self.web.switch_to.window(self.web.window_handles[-1])
                        except:
                            self.log.emit("打开视频失败，可能是对应编号的视频不存在！")
                    elif com == 0xfe: # 退出程序
                        self.par.bilibiliRunning.clear()
                        self.quit_thread()
                    elif com == 0xff: # 退出视频
                        self.web.close()
                        self.web.switch_to.window(self.web.window_handles[0])
                        if len(self.web.window_handles) == 0: # 关闭后如果再没有窗口，则直接关闭
                            self.par.bilibiliRunning.clear()
                            self.quit_thread()
                    else:
                        self.log.emit(f"指令 {com.to_bytes().hex()} 不符合编码规范，执行失败")
                else:
                    self.log.emit(f"数据包头不符合编码规范，指令执行失败！")
            else:
                sleep(0.1)
            

        self.quit_thread()
    
    def quit_thread(self):
        if self.web.session_id is not None:
            self.log.emit("bilibiliThread 结束运行")
            self.web.quit()

if __name__ == "__main__":
    app = QApplication()
    win = APPWindow(app)
    win.show()
    app.exec()