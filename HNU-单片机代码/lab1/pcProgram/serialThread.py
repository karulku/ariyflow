import serial
from PySide6.QtCore import QThread, Signal
from threading import Event
from PySide6.QtWidgets import QMessageBox
BYTE_NUM = 8

class serialThread(QThread):
    log = Signal(str)
    read_data = Signal(bytes)
    def __init__(self, par):
        super().__init__()
        self.par = par
        self.ser = serial.Serial()
        self.is_running = Event()
        self.is_running.clear()
    
    def run(self):
        self.log.emit("serialThread开始运行")
        while self.is_running.is_set():
            if not self.ser or not self.ser.is_open:
                self.msleep(1000)
                continue
            
            reading = self.ser.read(BYTE_NUM)
            if reading and reading[0] == 0xaa and reading[1] == 0x55:
                self.read_data.emit(reading)
                self.log.emit(f"接收数据: {reading.hex()}")
            else:
                self.log.emit(f"未收到数据包，继续轮询...")
            self.msleep(100)
        
        self.log.emit("serialThread运行结束")
    
    def open_serial(self, port, baudrate, timeout):
        if self.ser and self.ser.is_open:
            QMessageBox.about(None, "提示", "串口已打开！")
            return
        try:
            self.ser.port = port
            self.ser.baudrate = baudrate
            self.ser.timeout = timeout
            self.ser.open()
            self.log.emit("串口打开成功！")
        except Exception as e:
            QMessageBox.about(None, "提示", f"串口打开失败！\n{e}")
    
    def close_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log.emit("串口已关闭！")
        else:
            QMessageBox.about(None, "提示", f"串口未打开或不存在！")
    
    def send_data(self, data: bytes):
        if self.ser and self.ser.is_open:
            self.ser.write(data)
            self.log.emit(f"发送: {data.hex()}")