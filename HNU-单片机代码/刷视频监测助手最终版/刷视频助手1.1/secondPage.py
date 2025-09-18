from PySide6.QtWidgets import(
    QWidget,QLCDNumber,QLabel,QMessageBox,QPushButton
)
from PySide6.QtCore import QTimer, Signal
from datetime import datetime, timedelta
from threading import Event
import math
from typing import cast
ADC_TIMEOUT = 10000
NORMAL_TIMEOUT = 1000

class secondPage(QWidget):
    log = Signal(str)
    def __init__(self, par):
        super().__init__()
        self.par = par
        self.page = self.par.findChild(QWidget, "second_page") # type: QWidget
        self.light_dense = 50 # 该变量接收并保存从单片机传来的光照强度
        self.tempreture = 25 # 接收温度
        self.fm_frequency = 918
        self.fm_volume = 5
        # print(self.par,self.page)
        self.load_widgets()
        
        self.par.pipe.connect(self.get_data)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(NORMAL_TIMEOUT) # 启动定时，每1秒调用update函数
        self.update_time()
        
        self.adc_timer = QTimer(self)
        self.adc_timer.timeout.connect(self.adcEvent)
        self.adc_timer.start(ADC_TIMEOUT) # adc时间定时
        self.adc_enable = Event()
        self.adcEvent()
    
    def load_widgets(self):
        self.lcd = self.page.findChild(QLCDNumber, "lcd")
        self.date_label = self.page.findChild(QLabel, "date_label")
        self.light_intensity = self.page.findChild(QLabel, "light_intensity")
        self.tem_label = self.page.findChild(QLabel, "tem_label")
        self.sync_btn = self.page.findChild(QPushButton, "sync_btn")
        
        self.fm_frequency_label = self.page.findChild(QLabel, "fm_frequency_label")
        self.fm_volume_label = self.page.findChild(QLabel, "fm_volume_label")
        # print(self.fm_frequency_label,self.fm_volume_label)
      
        self.lcd.setDigitCount(8) # type: ignore
        self.sync_btn = cast(QPushButton, self.sync_btn)
        self.sync_btn.clicked.connect(self.syncEvent)
    
    # 定时器timer绑定的函数，每1s执行一次
    def update_time(self):
        now_time = datetime.now().replace(microsecond=0)
        self.lcd.display(f"{now_time.hour:02d}:{now_time.minute:02d}:{now_time.second:02d}") # type: ignore
        self.date_label.setText(f"{now_time.year}年{now_time.month}月{now_time.day}日，星期{self.ark(now_time.weekday())}") # type: ignore
        self.light_intensity.setText(str(self.light_dense)) # type: ignore
        self.tem_label.setText(str(self.adcToTem(self.tempreture))+"℃") # type: ignore
        self.fm_frequency_label.setText(f"当前频率：{self.fm_frequency/10}") # type: ignore
        self.fm_volume_label.setText(f"当前音量：{self.fm_volume}") # type: ignore
        
    # 定时器adc_timer绑定的函数，计划每10s执行一次
    def adcEvent(self):
        if self.adc_enable.is_set():
            return
        self.adc_enable.set()
        if self.light_dense < 20:
            print("\a")
            QMessageBox.about(None,"警告","当前环境较暗，注意保护眼睛哦！")
        elif self.light_dense > 80:
            print("\a")
            QMessageBox.about(None, "警告","当前环境较亮，注意保护眼睛哦！")
        else:
            pass
        self.adc_enable.clear()
    
    # 星期译码表
    def ark(self, idx):
        self.ark_list = ["一","二","三","四","五","六","日"]
        return self.ark_list[idx]
    
    # 从管道获取数据的函数
    def get_data(self, data: bytes):
        self.data = data
        self.execute()
    
    # 获取到数据包后的执行函数
    def execute(self):
        if self.data and self.data[0] == 0x01: # 符合规范
            # self.send_log(f"收到数据包：{self.data.hex()}")
            if self.data[1] == 0x00: # 接收adc数模转换值
                if self.data[2] == 0x00: # 光照强度adc
                    self.light_dense = int.from_bytes(self.data[-3:-1])
                elif self.data[2] == 0x01: # 温度adc
                    self.tempreture = int.from_bytes(self.data[-3:-1])
            elif self.data[1] == 0x01: # 接收FM收音机信息
                self.fm_frequency = int.from_bytes(self.data[2:4])
                self.fm_volume = self.data[4]
    
    # 发送日志的函数
    def send_log(self, content):
        self.log.emit("secondPage:"+content)
    
    # 温度adc值转换的函数
    def adcToTem(self, tem: int):
        vccx = tem/1000
        lnx = math.log(vccx/(1-vccx))
        t = 1/((lnx/3950)+(1/298.15)) - 273.15
        return round(t, 1)

    # 同步时钟的信号
    def syncEvent(self):
        self.synct = datetime.now()
        self.syncTimer = QTimer()
        self.syncTimer.timeout.connect(self.send_sync_data)
        self.syncTimer.start(100)
        self.syncCnt = 0

    
    # 辅助函数，传递某些时钟信息
    def send_sync_data(self):
        self.synct = datetime.now()
        if self.syncCnt == 3:
            self.syncTimer.stop()
            self.syncCnt = 0
            return
        elif self.syncCnt == 0:
            data = b"\x10\x29\x01\01\00"+(self.synct.year-2000).to_bytes(1)+self.synct.month.to_bytes(1)+self.synct.day.to_bytes(1)
            self.par.serialThread.send_data(data)
        elif self.syncCnt == 1:
            data = b"\x10\x29\x01\01\01"+(self.synct.hour).to_bytes(1)+self.synct.minute.to_bytes(1)+self.synct.second.to_bytes(1)
            self.par.serialThread.send_data(data)
        elif self.syncCnt == 2:
            data = b"\x10\x29\x01\01\02"+self.synct.weekday().to_bytes(1)+b"\x00\x00"
            self.par.serialThread.send_data(data)
        self.syncCnt += 1