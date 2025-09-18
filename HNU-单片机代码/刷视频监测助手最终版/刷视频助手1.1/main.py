from PySide6.QtCore import QFile, QThread, QMutex, Signal
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QTabWidget, QWidget, QComboBox, QLineEdit,
    QPushButton, QPlainTextEdit, QMessageBox, QFileDialog
)
from PySide6.QtUiTools import QUiLoader
from serialThread import serialThread
from bilibiliThread import bilibiliThread
from firstPage import firstPage
from datetime import datetime
from threading import Event
from secondPage import secondPage
import time
import json

class VideoAssistant(QMainWindow):
    pipe = Signal(bytes) # 用于传递指令的管道
    def __init__(self, app: QApplication):
        super().__init__()
           
        self.win = QUiLoader().load(QFile("./A03.ui"))
        self.setCentralWidget(self.win)
        self.setWindowTitle("刷视频助手1.0")
        self.setGeometry(300,200,1080,720)
        
        self.app = app
        self.app.aboutToQuit.connect(self.quitAppEvent) # 在退出时调用quitApp函数
        
        self.tabWidget = self.win.findChild(QTabWidget,"tabWidget") # tab标签
        self.currentTabIndex = self.tabWidget.currentIndex()# 变量记录当前标签页的索引 # type: ignore 
        self.tabWidget.currentChanged.connect(self.tabChangedEvent) # type: ignore
        
        self.load_global_widgets()
        # print(self.serial_name.text(), self.baudrate_select.currentText(), self.delay_time.currentText()) # type: ignore
        self.serialThread = serialThread(self.serial_name.text(), int(self.baudrate_select.currentText()), float(self.delay_time.currentText()[:-1])) # type: ignore
        self.serialThread.data.connect(self.data_parse) # data处接收传来的数据并处理
        self.serialThread.log.connect(self.tprint)
        self.serialThread.start()
        
        # 程序开始后尝试打开一次串口
        try:
            self.serialThread.open_serial(self.serial_name.text(), int(self.baudrate_select.currentText()), float(self.delay_time.currentText()[:-1])) # type: ignore
        except:
            self.tprint("自动打开串口失败！尝试手动打开串口")
        self.bindBtnEvent()
        
        # 刚刚打开时为第一个页面，开启bilibili线程
        self.bilibiliThread = bilibiliThread(self)
        self.bilibiliThread.log.connect(self.tprint)
        self.bilibiliThread.timeout_signal.connect(self.timeout_event)
        self.bilibiliThread.start()
        
        self.is_send_timeout = Event()
        self.is_send_timeout.clear()
        
        # 后面加载各个页面的组件
        self.firstPage = firstPage(self)
        self.secondPage = secondPage(self)
        
        self.secondPage.log.connect(self.tprint)
    
    def tabChangedEvent(self, index):
        # 这里放对原先page的处理
        if self.currentTabIndex == 0:
            # 如果原先页面为page1，暂停其运行
            self.bilibiliThread.is_paused.set()
        
        self.currentTabIndex = index
        # 这里放对当前page的处理
        if self.currentTabIndex == 0:
            # 取消暂停
            self.bilibiliThread.is_paused.clear()
    
    def quitAppEvent(self):
        # 这里处理退出逻辑
        
        # 退出bilibili线程
        if self.bilibiliThread and self.bilibiliThread.isRunning():
            self.bilibiliThread.close_thread()
        
        # 退出串口通信
        if self.serialThread and self.serialThread.isRunning():
            self.serialThread.is_running.clear()
            self.serialThread.quit()
            self.serialThread.wait()
            if self.serialThread.ser and self.serialThread.ser.is_open:
                self.serialThread.ser.close()
    
    def load_global_widgets(self):
        self.first_page = self.win.findChild(QWidget, "first_page")
        
        self.baudrate_select = self.first_page.findChild(QComboBox,"baudrate_select") # type: ignore
        self.serial_name = self.first_page.findChild(QLineEdit,"serial_name") # type: ignore
        self.delay_time = self.first_page.findChild(QComboBox,"delay_time") # type: ignore
        self.open_serial_btn = self.first_page.findChild(QPushButton,"open_serial_btn") # type: ignore
        self.close_serial_btn = self.first_page.findChild(QPushButton,"close_serial_btn") # type: ignore
        self.exit_app_btn = self.first_page.findChild(QPushButton,"exit_app_btn") # type: ignore

        self.clear_log_btn = self.first_page.findChild(QPushButton,"clear_log_btn") # type: ignore
        self.save_log_btn = self.first_page.findChild(QPushButton,"save_log_btn") # type: ignore
        self.message_text = self.first_page.findChild(QPlainTextEdit,"message_text") # type: ignore
    
    def bindBtnEvent(self):
        self.open_serial_btn.clicked.connect(self.open_serial_event) # type: ignore
        self.close_serial_btn.clicked.connect(self.close_serial_event) # type: ignore
        self.exit_app_btn.clicked.connect(self.exit_app_event) # type: ignore
        self.clear_log_btn.clicked.connect(self.clear_log_event) # type: ignore
        self.save_log_btn.clicked.connect(self.save_log_event) # type: ignore
    
    def open_serial_event(self):
        if self.serialThread.ser.is_open:
            QMessageBox.about(None, "提示", "串口已打开！")
            return
        else:
            self.serialThread.open_serial(self.serial_name.text(), int(self.baudrate_select.currentText()), float(self.delay_time.currentText()[:-1])) # type: ignore
            self.tprint("打开串口成功！")
    def close_serial_event(self):
        if not self.serialThread.ser.is_open:
            QMessageBox.about(None, "提示", "串口已关闭！")
            return
        else:
            self.serialThread.close_serial()
            self.tprint("关闭串口成功！")
    def exit_app_event(self):
        self.quitAppEvent()
        self.app.quit()

    def clear_log_event(self):
        select = QMessageBox.question(None, "提示", "确认清空日志？",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if select == QMessageBox.StandardButton.Yes:
            self.message_text.clear() # type: ignore
            
    
    def save_log_event(self):
        try:
            location = QFileDialog.getExistingDirectory(self,"日志保存位置")
            if location != "":
                now_time = datetime.now()
                file_name = f"firstPage_log_{now_time.year}_{now_time.month}_{now_time.day}_{now_time.hour}_{now_time.minute}_{now_time.second}"
                with open(f"{location}/{file_name}.log",mode="w",encoding="utf-8") as file:
                    file.write(self.message_text.toPlainText().strip()) # type: ignore
                QMessageBox.about(None,"提示",f"日志成功保存到：\n{location}/{file_name}.log")
        except Exception as e:
            QMessageBox.warning(None,"提示","未知错误，日志保存失败！")
    
    def data_parse(self, data: bytes):
        if data[0] == 0x00:
            self.tprint(f"page 1指令：{data[1:].hex()}")
        elif data[0] == 0x01:
            # 取消辅助功能页的log
            # self.tprint(f"page 2指令：{data[1:].hex()}")
            pass
        elif data[0] == 0x02: # 上位机->PC
            self.tprint(f"上位机指令：{data[1:].hex()}")
            self.hostCommandParse(data)
        else:
            print(f"无效指令！（{data.hex()}）")
            
        self.pipe.emit(data) # 这里直接向所有接收pipe的线程发送指令，根据第一个字节来确定谁要接收数据
    
    def tprint(self, log: str):
        self.message_text.appendPlainText(log) # type: ignore
    
    # 该超时信号仅用于page1
    def timeout_event(self):
        if self.is_send_timeout.is_set():
            return
        else:
            self.tprint("已超时，发送超时信号")
            data = b"\x10\x29\x00\x00\x04\x00\x00\x00"
            
            self.serialThread.send_data(data)
            # for _ in range(10):
            #     self.serialThread.send_data(data)
            #     time.sleep(0.1)
            #     reading = self.serialThread.ser.read(8)
            #     if reading and reading[2] == 0xff:
            #         break
                
            self.is_send_timeout.set()
    
    # 处理来自上位机的指令
    def hostCommandParse(self, data: bytes):
        # 这里的data有6个字节
        if data[1] == 0x00: # 修改下位机的超时时间
            hour,minute,second = data[2],data[3],data[4]
            new_settings = json.loads(open("./settings.json",mode="r",encoding="utf-8").read())
            new_settings["time_limit"] = (hour*3600+minute*60+second)
            with open("./settings.json", mode="w",encoding="utf-8") as file:
                file.write(json.dumps(new_settings))
    
if __name__ == "__main__":
    app = QApplication()
    win = VideoAssistant(app)
    win.show()
    app.exec()