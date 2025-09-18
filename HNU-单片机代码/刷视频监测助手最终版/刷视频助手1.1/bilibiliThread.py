from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow
from threading import Event
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json

TIME_LIMIT = 500 # 该处的值已被settings.json中的time_limit取代

class bilibiliThread(QThread):
    log = Signal(str)
    timeout_signal = Signal()
    log_head = "bilibiliThread: "
    def __init__(self, par):
        super().__init__()
        
        self.par = par
        self.data = b""
        self.cookie = """
        
        buvid3=0D3E1988-86C5-DC7A-92EE-5ED699FBBCA120001infoc; b_nut=1736084620; _uuid=5F9D145E-8A54-8885-6CB5-9B47147CBF7534625infoc; enable_web_push=DISABLE; buvid_fp=ac35f630292410286b12fb24d19dd76c; rpdid=|(kmJY~k|))R0J'u~JY|)R~Jl; hit-dyn-v2=1; LIVE_BUVID=AUTO7917360874195812; is-2022-channel=1; enable_feed_channel=ENABLE; fingerprint=1050de901c2356c41cc34246a87adfc5; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; DedeUserID=520005682; DedeUserID__ckMd5=e94e24c011776c20; header_theme_version=OPEN; CURRENT_QUALITY=80; buvid4=A23ABFAC-2937-B612-90E1-F52C56E90E4C02339-023092920-PdJr0jKE6N7dIAPqNjcZdnzZqsaY1n9f+rcGU3sETMY%3D; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTgxOTAyNjUsImlhdCI6MTc1NzkzMTAwNSwicGx0IjotMX0.IZclqe_kWbHewGakXaniGRzAEHs3Tff7Jmr24EzAQZw; bili_ticket_expires=1758190205; PVID=1; SESSDATA=ccad2a99%2C1773578311%2C75080%2A92CjATpxnqOUBdiEWagX-DtInXzHnlLoctt2T_Qrf60DiNJXA21K_VfLeL-C97ocizmOgSVnpwNE9kLWRpUEd4T2xiaGVJLTFobUI5QzNFOGE1SEZxSmR3dk9QXzBjQVRvVzZXNlBoZ0hSUk1leXgzMGJMYWx0cDR1Rl9ScW5IWEUxSVNMX21hcHVnIIEC; bili_jct=b0d8d07f2b9f396f21621039bd2c3290; sid=57ezm2pu; CURRENT_FNVAL=2000; bp_t_offset_520005682=1113579754499342336; b_lsid=233B1976_1995BB57D3C; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; home_feed_column=4; browser_resolution=593-941
        
        """
        self.par.pipe.connect(self.get_data)
        self.is_running = Event()
        self.is_running.set()
        self.is_paused = Event()
        self.is_paused.set()
        
        self.web = None
        self.url = "https://www.bilibili.com"

        self.settings = json.loads(open("./settings.json", mode="r",encoding="utf-8").read())
        self.TIME_LIMIT = self.settings["time_limit"]
    
    def run(self):
        self.log.emit(self.log_head+"开始运行")
        # self.web.maximize_window()
        self.start_time = time.time()
        while self.is_running.is_set():
            if self.is_paused.set():
                self.msleep(100)
                continue
            
            if self.data and self.data[0] == 0x00:
                if self.data[2] == 0x00:
                    if self.data[1] == 0x00:
                        self.refresh_bilibili()
                    elif self.data[1] == 0xff:
                        self.close_video()
                    elif self.data[1]>= 0x01 and self.data[1]<= 0x06:
                        self.open_video(self.data[1]-1)
                    elif self.data[1] == 0xfe:
                        self.quit_all()
                    else:
                        self.log.emit(f"bilibiliThread: 无效指令：{self.data.hex()}")
                elif self.data[2] == 0x01:
                    self.open_bilibili()
                else:
                    self.log.emit(f"bilibiliThread: 无效指令：{self.data.hex()}")
                
                self.data = b""
            
            self.now_time = time.time()
            self.delta_time = self.now_time - self.start_time
            # print(self.delta_time, self.TIME_LIMIT)
            if self.delta_time > self.TIME_LIMIT:
                self.timeout_signal.emit()
            self.msleep(100)

    def close_thread(self):
        self.is_running.clear()
        self.quit()
        self.wait()
        
        # 退出线程后，向串口发送总时间
        self.now_time = time.time()
        self.delta_time = self.now_time - self.start_time
        data = b"\x10\x29\x00\x00\x03"+int(self.delta_time/3600).to_bytes()+int(self.delta_time%3600/60).to_bytes()+int(self.delta_time%60).to_bytes()
        # print(data.hex())
        if self.par.serialThread.ser and self.par.serialThread.ser.is_open:
            self.par.serialThread.send_data(data)
        # for _ in range(5):
        #     self.par.serialThread.send_data(data)
        #     time.sleep(0.1)
        #     reading = self.par.serialThread.ser.read(8)
        #     if reading and reading[2] == 0xff:
        #         break
    
    def get_data(self, data):
        self.data = data
        
    def add_cookie(self, cookie: str):
        self.cookie = cookie
        self.log.emit("cookie保存成功！")
    
    def open_bilibili(self):
        self.log.emit(self.log_head+"打开bilibili.")
        
        self.web = webdriver.Edge()
        self.web.get(self.url)
        
        cookie_list = []
        msg_list = self.cookie.split("; ")
        for msg in msg_list:
            k,v = msg.split("=")
            cookie_list.append({"name":k.strip(),"value":v.strip(),"domain":".bilibili.com"})
        
        for cookie in cookie_list:
            self.web.add_cookie(cookie)
        
        self.web.refresh()
        self.log.emit(self.log_head+" cookie加载完毕")
        
        self.web.maximize_window()
    
    def refresh_bilibili(self):
        self.log.emit(self.log_head+"刷新页面...")
        self.web.find_element(By.XPATH,"//button[@class='primary-btn roll-btn']").click() # type: ignore
    
    def close_video(self):
        self.log.emit(self.log_head+"关闭视频...")
        if len(self.web.window_handles) != 1: # type: ignore
            self.web.close() # type: ignore
            self.web.switch_to.window(self.web.window_handles[-1]) # type: ignore
        else:
            self.web.quit() # type: ignore
        
    def open_video(self, idx: int):
        self.log.emit(self.log_head+"打开视频...")
        video_list = self.web.find_elements(By.XPATH,"//div[@class='feed-card']") # type: ignore
        try:
            video_list[idx].click()
            self.web.switch_to.window(self.web.window_handles[-1]) # type: ignore
        except:
            self.log.emit(self.log_head+"打开视频失败，可能是对应编号的视频不存在！")
        
    def quit_all(self):
        self.log.emit(self.log_head+"关闭页面...")
        self.web.quit() # type: ignore
    