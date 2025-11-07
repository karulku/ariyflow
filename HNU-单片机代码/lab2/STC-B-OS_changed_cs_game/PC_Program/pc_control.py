import webbrowser
from serialThread import serialThread
import pydirectinput
import time
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By

class APP:
    url = "http://www.ariyflow.asia:5000/qian-ru-shi-lab2"
    web_turn = 0 # 当前要打开网页还是关闭网页
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        
        self.serialThread = serialThread(self.queue)
        self.serialThread.open_serial()
        self.serialThread.start()
        
    def data_parse(self):
        while True:
            data = self.queue.get()
            # print(f"处理数据：{data[2]}")
            command = data[2]
            if command == 0x00:
                if self.web_turn == 0:
                    self.web = webdriver.Edge()
                    self.web.get(self.url)
                    self.web.maximize_window()
                elif self.web_turn == 1:
                    self.web.close()
                self.web_turn = 1 - self.web_turn
            elif command == 0x01:
                pydirectinput.press("w")
            elif command == 0x02:
                pydirectinput.press("s")
            elif command == 0x03:
                pydirectinput.press("a")
            elif command == 0x04:
                pydirectinput.press("d")
            elif command == 0x05:
                pydirectinput.press("enter")
            elif command == 0x06:
                if self.web:
                    self.web.find_element(By.ID, "restart-btn").click()
                    self.web.find_element(By.XPATH, "//body").click()
            elif command == 0x07: # 退出程序
                self.serialThread.is_running.clear()
                return


if __name__ == "__main__":
    app = APP()
    app.data_parse()
    
    app.serialThread.join()