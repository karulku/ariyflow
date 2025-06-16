import requests
import re
import json
import os
import sys

def action(s:str):
    if s.count("\\") or s.count("/") or s.count(":") or s.count("*") or s.count("?") or s.count("?") or s.count("\"") or s.count("<") or s.count(">") or s.count("|"):
        s.replace("\\","").replace("/","").replace(":","").replace("*","").replace("?","").replace("\"","").replace("<","").replace(">","").replace("|","")
        print("windows文件名中不能包含以下符号： \\ / : * ? \" < > | \n已为您自动修改")
    return s

if len(sys.argv) != 3:
    print("输入参数有误，请检查！")
    print(sys.argv)
    exit(0)

url = sys.argv[2].strip("\"")

dat_obj = re.compile(r'<script>window.__playinfo__=(?P<dat>.*?)</script>',re.S)
name_obj = re.compile(r'<meta data-vue-meta="true" property="og:title" content="(?P<title>.*?)">',re.S)

headers = {
    # "referer":"https://www.bilibili.com/video/BV1XyMEzCE6u/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=f88ac9ccc2accccabd1e03f169793ecd",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "cookie":"buvid3=0D3E1988-86C5-DC7A-92EE-5ED699FBBCA120001infoc; b_nut=1736084620; _uuid=5F9D145E-8A54-8885-6CB5-9B47147CBF7534625infoc; enable_web_push=DISABLE; buvid_fp=ac35f630292410286b12fb24d19dd76c; DedeUserID=520005682; DedeUserID__ckMd5=e94e24c011776c20; rpdid=|(kmJY~k|))R0J'u~JY|)R~Jl; hit-dyn-v2=1; LIVE_BUVID=AUTO7917360874195812; buvid4=A23ABFAC-2937-B612-90E1-F52C56E90E4C02339-023092920-PdJr0jKE6N7dIAPqNjcZdnzZqsaY1n9f%2BrcGU3sETMY%3D; is-2022-channel=1; enable_feed_channel=ENABLE; PVID=1; CURRENT_QUALITY=0; fingerprint=1050de901c2356c41cc34246a87adfc5; home_feed_column=5; browser_resolution=1699-941; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTAwNzg2MTQsImlhdCI6MTc0OTgxOTM1NCwicGx0IjotMX0.wvPnP3ZICLKI89k-inXxPst6rTMlscQDKn6VOgTpq7M; bili_ticket_expires=1750078554; SESSDATA=4893952b%2C1765547982%2C95425%2A62CjB3BufqUCpFNHma5FWHtGgwnb33iLmy6R_yfRx_PycE4IlLjPAnbKqMbhRlUs9PxVMSVlBDbGVqc1ZlMG1UZ2ZoX2VSX3dfRnI1LXQ2UWppTzZyRlNiTXN4Qy05TndwMlhJbzljQjRqeHJMRDRSU2g1QzA2SVVCZ2JlV0NtZDhjNXZEaWhfS2N3IIEC; bili_jct=3835cc1441231e04f5229bfad7444476; sid=7z1lakm0; b_lsid=6510973D7_19776C9378C; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; bp_t_offset_520005682=1078934203237662720; timeMachine=0; CURRENT_FNVAL=4048"
}

# 第一部分，从主页面拿到需要的信息
resp = requests.get(url,headers = headers)
resp.encoding = "utf-8"
print("响应码：",resp.status_code)
name = name_obj.search(resp.text)
try:
    if name:
        name = action(name.group("title"))
        print(f"获取到视频标题：{name}")
    else:
        print("未获取到视频标题，将使用output代替！")
        name = "output"
except:
    print("视频标题中可能存在表情等字符，无法输出到终端")
dat = dat_obj.search(resp.text)
if dat:
    dat = dat.group("dat")
else:
    print("error: 未找到信息！")
    exit(1)
dat = json.loads(dat)["data"]
id = dat["dash"]["video"][0]["id"]
if id <80 :
    print("提示：视频清晰度较低，注意甄别")
resp.close()


video_headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "referer":url
}
# 第二部分，根据前面拿到的信息获取视频
cnt = 0
while True:
    try:
        print("开始获取视频...")
        base_url = dat["dash"]["video"][cnt]["baseUrl"]
        print(f"找到视频url: {base_url}")
        print("视频爬取过程较慢，请耐心等待...")
        resp = requests.get(base_url,headers=video_headers)
        print(f"视频url响应码：{resp.status_code}")
        if resp.status_code == 200:
            with open("video.mp4",mode="wb") as file:
                file.write(resp.content)
                print("视频保存成功！")
                break
        else:
            print("视频url响应失败，尝试其他url...")
            cnt+=1
            resp.close()
    except:
        print("所有视频清晰度均无法爬取！退出程序")
        resp.close()
        exit(-1)
resp.close()

# 根据前面的信息获取音频
cnt = 0
while True:
    try:
        print("开始爬取音频...")
        audio_url = dat["dash"]["audio"][cnt]["baseUrl"]
        print(f"找到音频url: {audio_url}")
        audio_resp = requests.get(audio_url)

        if audio_resp.status_code == 200:
            print("音频url请求成功！")
            with open("audio.mp3",mode="wb") as file:
                file.write(audio_resp.content)
                print("音频保存成功！")
                break
        else:
            print(f"音频请求失败，错误码：{audio_resp.status_code} 即将更换url重试...")
            cnt+=1
            audio_resp.close()
    except:
        print("所有音频均无法获取！")
        audio_resp.close()
        break
    audio_resp.close()

print("开始合并视频和音频...")
os.system(f"ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \"./spider_videos/{name}.mp4\"")

os.remove("video.mp4")
os.remove("audio.mp3")

print("爬取视频结束！")