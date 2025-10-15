from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QComboBox,
    QPlainTextEdit, QLineEdit, QMessageBox, QGroupBox
)

from PySide6.QtCore import QFile, QThread, Signal, QTimer
from PySide6.QtUiTools import QUiLoader
from datetime import datetime
import sys
from serialThread import serialThread
from matThread import matThread
import struct
import math
import pymysql

"""
aa 55 xa xb xc xd xe 00
xa - 步进电机选择 xb - 速度 xc - 加速度 xd - 转动方向 xe - 平缓加速

第2字节为03时，表示传输其他指令
03 -- 传输指令
    00 xa xb 00 00 # update步数，调用该函数后，会将所有步进电机步数设置为60000
"""

class smApp(QMainWindow):
    def __init__(self, par: QApplication):
        super().__init__()
        self.par = par
        
        self.win = QUiLoader().load(QFile("version0.ui"))
        
        self.setCentralWidget(self.win)
        self.setWindowTitle("步进电机管理程序")
        self.setGeometry(300,200,1080,720)
        
        self.serialThread = serialThread(self)
        self.serialThread.log.connect(self.tprint)
        self.serialThread.read_data.connect(self.data_parse)
        self.serialThread.is_running.set()
        self.serialThread.start()
        
        self.matThread = matThread(self)
        
        self.par.aboutToQuit.connect(self.exit_app_event)

        self.load_widgets()
        
        # 保存传来的一些数据
        self.tem = 0
        self.light = 0
        
        self.sqlTimer = QTimer()
        self.sqlTimer.timeout.connect(self.sqlTimerTimeout)
        self.sqlTimer.start(1000)
        
        # 打开数据库
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="526122",
            database="test_db",
            charset="utf8mb4"
        )
        
        self.cur = self.conn.cursor()
        
        # 开始时尝试打开一次串口
        try:
            self.serialThread.ser.port = "COM3"
            self.serialThread.ser.baudrate = 9600
            self.serialThread.ser.timeout = 1
            self.serialThread.ser.open()
            self.tprint("串口打开成功！")
        except:
            pass
        
    def load_widgets(self):
        self.sm_setting_box = self.win.findChild(QGroupBox, "sm_setting_box")
        self.serial_setting_box = self.win.findChild(QGroupBox, "serial_setting_box")
        self.sm0_box = self.win.findChild(QGroupBox, "sm0_box")
        self.sm1_box = self.win.findChild(QGroupBox, "sm1_box")
        self.sm2_box = self.win.findChild(QGroupBox, "sm2_box")
        self.log_plain = self.win.findChild(QPlainTextEdit, "log_plain")
        
        # 串口设置栏
        self.baudrate_select = self.serial_setting_box.findChild(QComboBox, "baudrate_select") # type: ignore
        self.port_name = self.serial_setting_box.findChild(QLineEdit, "port_name") # type: ignore
        self.timeout_select = self.serial_setting_box.findChild(QComboBox, "timeout_select") # type: ignore
        
        self.open_serial_btn = self.serial_setting_box.findChild(QPushButton, "open_serial_btn") # type: ignore
        self.close_serial_btn = self.serial_setting_box.findChild(QPushButton, "close_serial_btn") # type: ignore
        self.exit_btn = self.serial_setting_box.findChild(QPushButton,"exit_btn") # type: ignore
        
        self.open_serial_btn.clicked.connect(self.open_serial_event) # type: ignore
        self.close_serial_btn.clicked.connect(self.close_serial_event) # type: ignore
        self.exit_btn.clicked.connect(self.exit_app_event) # type: ignore
        
        # 步进电机设置栏
        self.sm_select = self.sm_setting_box.findChild(QComboBox, "sm_select") # type: ignore
        self.sm_speed = self.sm_setting_box.findChild(QLineEdit, "sm_speed") # type: ignore
        self.sm_acc = self.sm_setting_box.findChild(QLineEdit, "sm_acc") # type: ignore
        self.sm_dir = self.sm_setting_box.findChild(QComboBox, "sm_dir") # type: ignore
        self.sm_smooth_speed = self.sm_setting_box.findChild(QLineEdit, "sm_smooth_speed") # type: ignore
        self.send_btn = self.sm_setting_box.findChild(QPushButton, "send_btn") # type: ignore
        self.reset_step_btn = self.sm_setting_box.findChild(QPushButton, "reset_step_btn") # type: ignore
        self.mat_btn = self.sm_setting_box.findChild(QPushButton, "mat_btn") # type: ignore
        
        
        self.mat_btn.clicked.connect(self.mat_event) # type: ignore
        self.send_btn.clicked.connect(self.send_command) # type: ignore
        self.reset_step_btn.clicked.connect(self.reset_step_event) # type: ignore
        
        # 状态栏
        self.tem_label = self.win.findChild(QLabel, "tem_label")
        self.light_label = self.win.findChild(QLabel, "light_label")
    
    def open_serial_event(self):
        port = self.port_name.text() # type: ignore
        baudrate = int(self.baudrate_select.currentText()) # type: ignore
        timeout = float(self.timeout_select.currentText()[:-1]) # type: ignore

        self.serialThread.open_serial(port, baudrate, timeout)
    
    def close_serial_event(self):
        self.serialThread.close_serial()
    
    def exit_app_event(self):
        
        if self.cur.connection and self.cur.connection.open:
            self.cur.close()
        if self.conn.open:
            self.conn.close()
        
        
        if self.serialThread.isRunning():
            self.serialThread.is_running.clear()
            if self.serialThread.ser and self.serialThread.ser.is_open:
                self.serialThread.close_serial()
            self.serialThread.quit()
            self.serialThread.wait()
        
        self.par.quit()
    
    def send_command(self):
        try:
            sm = self.sm_select.currentIndex() # type: ignore
            speed = int(self.sm_speed.text()) # type: ignore
            dir = self.sm_dir.currentIndex() # type: ignore
            
        except:
            QMessageBox.about(None, "提示", "请正确输入信息！")
        
        # 加入边界检验
        if self.sm_acc.text(): # type: ignore
            acc = int(self.sm_acc.text()) # type: ignore
        else:
            acc = 0xff
        
        if self.sm_smooth_speed.text(): # type: ignore
            smooth_speed = int(self.sm_smooth_speed.text()) # type: ignore
        else:
            smooth_speed = 0xff
        
        if speed < 1 or speed > 255 or smooth_speed < 0 or smooth_speed > 255:
            QMessageBox.about(None, "提示", "速度超出范围！")
            return
        if (acc < -10 or (acc > 10 and acc != 0xff)):
            QMessageBox.about(None, "提示", "加速度超出范围！")
            return
        
        data: bytes = b"\xaa\x55"+sm.to_bytes(1, "big")+speed.to_bytes(1, "big")+(struct.pack('b', acc) if acc != 0xff else b'\xff')+dir.to_bytes(1, "big")+smooth_speed.to_bytes(1, "big")+b"\x00"
        self.serialThread.send_data(data)
    
    def tprint(self, log):
        self.log_plain.appendPlainText(log) # type: ignore
    
    # 需要补充接收到数据后的处理
    def data_parse(self, data: bytes):
        if data[2] >= 0 and data[2] <= 2: # 该条指令为对步进电机的操作
            idx = data[2]
            speed = data[3]
            acc = struct.unpack('b', data[4].to_bytes(1, "big"))[0]
            dir = data[5]
            rest_step = int.from_bytes(data[6:], byteorder="big")
            sm_boxes = [self.sm0_box, self.sm1_box, self.sm2_box]
            
            sm_boxes[idx].findChild(QLabel, f"sm{idx}_speed").setText(f"速度：{speed}") # type: ignore
            sm_boxes[idx].findChild(QLabel, f"sm{idx}_acc").setText(f"加速度：{acc}") # type: ignore
            sm_boxes[idx].findChild(QLabel, f"sm{idx}_dir").setText(f"转动方向：{dir}") # type: ignore
            sm_boxes[idx].findChild(QLabel, f"sm{idx}_rest_step").setText(f"剩余步数：{rest_step}") # type: ignore
        elif data[2] == 0x03:
            self.tem = int.from_bytes(data[3:5],byteorder="big")
            self.light = int.from_bytes(data[5:7])
            
            self.tem_label.setText(f"温度：{self.adcToTem(self.tem)}℃") # type: ignore
            self.light_label.setText(f"光照：{self.light}") # type: ignore
            
    # 温度adc值转换的函数
    def adcToTem(self, tem: int):
        try:
            vccx = tem/1000
            lnx = math.log(vccx/(1-vccx))
            t = 1/((lnx/3950)+(1/298.15)) - 273.15
            return round(t, 1)
        except:
            return 25.0
    
    def reset_step_event(self):
        data = b"\xaa\x55\x03\x00\xea\x60\x00\x00"
        self.serialThread.send_data(data)
    
    def get_time(self):
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
    
    # 每1s执行一次保存
    def sqlTimerTimeout(self):
        # print(self.adcToTem(self.tem), self.light)
        try:
            com = f"insert into step_msg (date, temperature, illumination) values ('{self.get_time()}',{self.adcToTem(self.tem)},{self.light});"
            self.cur.execute(com)
            self.conn.commit()
            self.tprint(f"数据库更新信息：{self.get_time()}',{self.adcToTem(self.tem)},{self.light}")
        except:
            self.tprint(f"数据库信息更新失败！")
    
    def mat_event(self):
        self.matThread.show()
                
        


if __name__ == "__main__":
    app = QApplication()
    win = smApp(app)
    win.show()
    sys.exit(app.exec())