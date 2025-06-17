import requests
import re
import json
import os
from lxml import etree
import sys

if len(sys.argv) < 2:
    print("参数输入有误，请检查！")
    exit(-1)

url = sys.argv[1]
cookie = ""
if len(sys.argv) >2:
    cookie = sys.argv[2]

# 能爬到一个视频就可以爬到所有视频，只需要把url改了就可以，这里我准备做一个GUI
playinfo_obj = re.compile(r'<script>window.__playinfo__=(?P<playinfo>.*?)</script>',re.S)
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "cookie":cookie # 浏览器的cookie是会失效的，想要爬取高清视频需要传入cookie，否则需要处理登录，非常麻烦，所以这里改成输入
}

# 第一部分，从视频页面中拿到保存信息的json
resp = requests.get(url,headers = headers)
resp.encoding="utf-8"

playinfo = playinfo_obj.search(resp.text).group("playinfo") # type: ignore
playinfo = json.loads(playinfo)

html = etree.HTML(resp.text,None)
title = html.xpath("//div[@class='video-info-title-inner']/h1/text()")[0]

resp.close()

# 第二部分，从json中提取视频文件和音频文件（b站音视频是分离的）
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "referer":url
}

cnt = 0
while True:
    try:
        # b站视频清晰度是有id的，对应的是这里的accept_quality和accept_description 比如id=80就是1080p
        video_url = playinfo["data"]["dash"]["video"][cnt]["baseUrl"]
        print(f"视频清晰度id: {playinfo["data"]["dash"]["video"][cnt]["id"]}")
        print("视频url:\n",video_url)
        resp = requests.get(video_url,headers=headers)
        if resp.status_code == 200:
            print("视频请求获取成功！")
            with open("video.m4s",mode="wb") as file:
                file.write(resp.content)
            resp.close()
            break
        else:
            print("视频获取失败！尝试降低清晰度重新获取！")
            cnt += 1
            resp.close()
    except:
        print("视频获取失败！程序退出。")
        resp.close()
        exit(-1)

# 音频和视频的方式一模一样
cnt = 0
while True:
    try:
        audio_url = playinfo["data"]["dash"]["audio"][cnt]["baseUrl"]
        print(f"音频清晰度id: {playinfo["data"]["dash"]["audio"][cnt]["id"]}")
        print("音频url:\n",audio_url)
        resp = requests.get(audio_url,headers=headers)
        if resp.status_code == 200:
            print("音频请求获取成功！")
            with open("audio.m4s",mode="wb") as file:
                file.write(resp.content)
            resp.close()
            break
        else:
            print("音频获取失败！尝试降低清晰度重新获取！")
            cnt += 1
            resp.close()
    except:
        print("音频获取失败！程序退出。")
        resp.close()
        exit(-1)

if not os.path.exists("./videos"):
    os.mkdir("./videos")
os.system(f"ffmpeg -i video.m4s -i audio.m4s -c copy ./videos/{title}.mp4")
os.remove("audio.m4s")
os.remove("video.m4s")
print("获取视频成功！")