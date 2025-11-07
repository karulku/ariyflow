import serial
from threading import Event, Thread
import queue
import time

class serialThread(Thread):
    def __init__(self, queue: queue.Queue):
        super().__init__()
        
        self.queue = queue
        
        self.ser = serial.Serial()
        self.is_running = Event()
        self.is_running.set()
    
    def run(self):
        while self.is_running.is_set():
            
            reading = self.ser.read(8)
            if reading and reading[0] == 0xaa and reading[1] == 0x55:
                self.queue.put(reading)
                print(f"收到数据：{reading[2]:02d}")
            
            time.sleep(0.1)
    
    def open_serial(self, port = "COM5", baudrate = 9600, timeout = 1):
        try:
            self.ser.port = port
            self.ser.baudrate = baudrate
            self.ser.timeout = timeout
            self.ser.open()
            print("串口打开成功！")
        except:
            print("串口打开失败")
    
    def close_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        else:
            print("串口未打开！")