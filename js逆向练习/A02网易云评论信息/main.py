import requests
import execjs
import json
"""
    网易的所有网页加密都是这一套逻辑，可以爬到评论就可以爬到其他所有网易公开的东西。
"""
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=8c85e894609cad636240e2989c8a09bf"

# 下面就需要把加密算法的结果获取到，这里我不分析加密的过程（因为不会）
# 直接把加密算法copy了
context = execjs.compile(open("code.js",mode="r",encoding="utf-8").read())


# 网易的加密算法需要四个参数，p1是要加密的信息，p2,p3,p4都是固定的字符串，注意第一个参数如果是json要转为字符串
# 我们只爬100页，做一个示例，应该是2000条评论
cnt = 0 # 评论的计数
page = 1 # 页面的计数
next_cursor = -1
for i in range(100):
    origin_data = {
        "csrf_token": "8c85e894609cad636240e2989c8a09bf",
        "cursor": f"{next_cursor}",
        "offset": "0",
        "orderType": "1",
        "pageNo": f"{page}",
        "pageSize": "20",
        "rid": "R_SO_4_2688129675",
        "threadId": "R_SO_4_2688129675"
    }

    tmp = context.call("getdata",origin_data)
    data = {
        "params":tmp["encText"],
        "encSecKey":tmp["encSecKey"]
    }

    resp = requests.post(url,data = data)

    # 第一页需要两个东西，一个是热评，一个是普通评论，剩下的页里面只有普通评论
    # 普通评论每页20条，热评总共有14条（大概）
    # 然后每页里面有一个cursor，作为传给下一个的参数，要拿下来
    content = json.loads(resp.text)
    next_cursor = content["data"]["cursor"]
    print("next_cursor:",next_cursor)

    if origin_data["cursor"] == "-1":
        hot_cnt = 0
        hotComments = content["data"]["hotComments"]
        print("热门评论：")
        hotComments = [item["content"] for item in hotComments]
        with open("hotComments.txt",mode="w",encoding="utf-8") as file:
            for hotcmt in hotComments:
                file.write(f"{hot_cnt:04d}{hotcmt.strip()}\n")
                hot_cnt+=1
        print("热门评论保存成功！")

    comments = content["data"]["comments"]
    comments = [item["content"] for item in comments]
    with open("comments.txt",mode="a",encoding="utf-8") as file:
        for cmt in comments:
            file.write(f"{cnt:04d}{cmt.strip()}\n")
            cnt += 1
    print(f"第 {page} 页评论保存成功！")
    # 这些评论好奇怪...
    resp.close()
    page += 1