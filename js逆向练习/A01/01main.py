# 第一个网站没了，所以就做网易云了
import requests
import execjs

def readfile(filename):
    with open(filename,mode="r",encoding="utf-8") as file:
        return file.read()

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=8c85e894609cad636240e2989c8a09bf"

# 处理加密
data = {
    "csrf_token":"8c85e894609cad636240e2989c8a09bf",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "3",
    "pageSize": "20",
    "rid": "R_SO_4_2715047901",
    "threadId": "R_SO_4_2715047901"
}

js_code = execjs.compile(readfile("code.js"))
rst = js_code.call("decrypt_data",data)

dat = {}
dat["params"] = rst["encText"]
dat["encSecKey"] = rst["encSecKey"]
print(dat)
resp = requests.post(url,data=dat)

print(resp.status_code)
print(resp.text)

resp.close()