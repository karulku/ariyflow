import serial
from PySide6.QtCore import QThread, QMutex, Signal
from threading import Event
from PySide6.QtWidgets import QMessageBox
BYTE_NUM = 8

# 在收到合法数据包后，会将数据包除包头外的6个字节发送到data
class serialThread(QThread):
    data = Signal(bytes)
    log = Signal(str)
    is_running = Event()
    
    def __init__(self, port, baudrate, timeout):
        super().__init__()
        self.is_running.set()
        self.ser = serial.Serial()
        self.log_head = "serialThread: "
    def run(self):
        while self.is_running.is_set():
            if self.ser and self.ser.is_open:
                reading = self.ser.read(BYTE_NUM)
                if reading and reading[0] == 0x10 and reading[1] == 0x29:
                    # 在辅助功能下，会有大量的串口读取，为了简化日志信息，这里取消辅助功能页的日志输出
                    self.log.emit(f"读取到合法数据包：{reading.hex()}")
                    self.data.emit(reading[2:])
                else:
                    self.log.emit(f"未读取到合法数据包，继续轮询...")
            self.msleep(100)

    def open_serial(self, port, baudrate, timeout):
        # 在没有打开串口时打开串口
        try:
            self.ser.port = port
            self.ser.baudrate = baudrate
            self.ser.timeout = timeout
            self.ser.open()
        except serial.SerialException as e:
            QMessageBox.about(None, "提示", "串口打开失败！")
    
    def close_serial(self):
        if self.ser.is_open:
            self.ser.close()
    
    def send_data(self, data: bytes, with_log = True):
        self.ser.write(data)
        if with_log == True:
            self.log.emit(self.log_head+f"发送数据包：{data.hex()}")