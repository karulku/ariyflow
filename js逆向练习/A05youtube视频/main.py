import requests
import re
import json
""" 代码没用，主要看下面的注释 这玩意对我来说难度还是太大了 """
# 使用yt-dlp下载：
## pip install yt-dlp
# 使用方法：yt-dlp "视频网址" 
# 生成字幕，使用whisper：
## pip install git+https://github.com/openai/whisper.git
#（audio.mp3可以使用ffmpeg [ffmpeg -i input.mp4 -vn -ar 44100 -ac 2 -ab 192k output.mp3]）
# whisper audio.mp3 --language English --task translate
# 将字幕加到视频中：
# ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" output.mp4
# 注意whisper生成的时间戳可能会有问题，或者单句字幕太长了，可能其他方法更合适

url = "https://www.youtube.com/watch?v=2BVqksYJ2yw"
headers = {}
playerinfo_obj = re.compile(r'var ytInitialPlayerResponse = (?P<playinfo>.*?);var',re.S)

resp = requests.get(url,headers = headers)
resp.encoding = "utf-8"
playinfo = playerinfo_obj.search(resp.text).group("playinfo") # type: ignore

json_data = json.loads(playinfo)
video_url = json_data["streamingData"]["adaptiveFormats"][0]["url"]

print(video_url)

resp.close()
