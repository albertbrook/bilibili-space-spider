# Spider for Bilibili Space
输入uid即可获得所有投稿的封面和相关信息
## 运行
运行需要导入三个库<br>
```python
import requests
import json
import os
```
requests是第三方库，需要额外安装，用来获取网页数据<br>
json是标准库，用来保存数据<br>
os是标准库，用来创建文件夹
## 获取数据
请求的url是
```python
"https://api.bilibili.com/x/space/arc/search?mid=25498927&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp".format(uid, page_number)
```
通过网络抓包工具很容易发现这个url，填入相应的url和页码就可以获得相关数据
## 保存数据
返回的是json字符串，转换成字典就可以读取想要的数据并保存了<br>
保存的时候，我先创建一个`uname(uid)`格式的文件夹
```python
name = "{}({})".format(json_data["author"], json_data["mid"])
os.mkdir(name)
```
然后根据av号创建相应的文件夹
```python
av = "av{}".format(json_data["aid"])
os.mkdir(av)
```
av号文件夹下保存相关数据和封面
```python
with open("{}/{}.json".format(av, av), mode="w", encoding="utf-8") as file:
    file.write(json.dumps(json_data, ensure_ascii=False))
with open("{}/{}".format(av, json_data["pic"].split("/")[-1]), mode="wb") as image:
    response = requests.get("https:{}".format(json_data["pic"]), headers=self.headers)
    image.write(response.content)
```
一些细节的处理就不赘述了，阅读源代码了解更多
## json字符串分析
以我自己的空间为例
```python
data = {
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": {
            "tlist": {
                "36": {
                    "tid": 36,
                    "count": 11,
                    "name": "科技"
                }
            },
            "vlist": []
        },
        "page": {
            "count": 11,
            "pn": 1,
            "ps": 30
        }
    }
}
```
前面三个键不重要，数据都在data里<br>
page：视频数量，页码，页面大小（每页的视频数量）<br>
可以根据page_number确定请求的次数<br>
tlist：各分区投稿数量，36就是科技区的tid了，舞蹈区的tid是129<br>
vlist：当前页码下的所有视频信息<br>
以我第一个视频为例
```python
data = {
    "comment": 918,
    "typeid": 122,
    "play": 230789,
    "pic": "//i2.hdslb.com/bfs/archive/7122d2104f1c01a13a9e3ee854566b4b65f5b1b9.jpg",
    "subtitle": "",
    "description": "如果成功整到了你的小伙伴记得给个硬币",
    "copyright": "",
    "title": "8分钟教你5个电脑上整人的方法",
    "review": 0,
    "author": "AlbertBrook",
    "mid": 25498927,
    "created": 1486063583,
    "length": "08:03",
    "video_review": 1126,
    "aid": 8365031,
    "bvid": "",
    "hide_click": False,
    "is_pay": 0,
    "is_union_video": 0
}
```
comment：评论数<br>
typeid：二级分区id，122就是野生技术协会了，20是宅舞<br>
play：播放数<br>
pic：封面地址<br>
subtitle：字幕<br>
description：简介内容<br>
copyright：版权<br>
title：标题<br>
review：是否审查中<br>
author：up主的名字<br>
mid：up主的uid<br>
created：时间戳，记录发布时间<br>
length：时长<br>
aid：av号<br>
is_pay：是否付费<br>
is_union_video：是否合作<br>
这三个还不清楚<br>
video_review<br>
bvid<br>
hide_click