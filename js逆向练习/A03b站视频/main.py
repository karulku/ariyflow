import subprocess
import os
while True:
    url = input("请输入url: ")
    name = "日志信息"
    os.remove("日志信息.log")
    with open(f"{name}.log",mode="a",encoding="utf-8") as file:
        spider_stream = subprocess.Popen(["python","./video_spider.py",name,"\""+url+"\""],stdout=file,stderr=file)
        print(f"视频开始爬取，视频爬取结束后，会将过程保存在：“{name}.log” 请耐心等待...")