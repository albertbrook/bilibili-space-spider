import requests
import json
import os


class Bss(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.json_list = []

    def get_url(self):
        uid = input("uid = ")
        url = "https://api.bilibili.com/x/space/arc/search?mid={}" \
              "&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp"
        self.add_json(url.format(uid, 1))
        max_page = (self.json_list[0]["data"]["page"]["count"] //
                    self.json_list[0]["data"]["page"]["ps"] + 1)
        if max_page > 1:
            for i in range(2, max_page + 1):
                self.add_json(url.format(uid, i))

    def add_json(self, url):
        response = requests.get(url, headers=self.headers)
        json_dict = json.loads(response.content.decode())
        self.json_list.append(json_dict)

    def save_data(self):
        name = self.get_user_name()
        try:
            os.mkdir(name)
        except FileExistsError:
            pass
        os.chdir(name)
        for json_dict in self.json_list:
            for json_data in json_dict["data"]["list"]["vlist"]:
                self.save_file(json_data)

    def get_user_name(self):
        for json_dict in self.json_list:
            for json_data in json_dict["data"]["list"]["vlist"]:
                if not json_data["is_union_video"]:
                    name = "{}({})".format(json_data["author"], json_data["mid"])
                    return name

    def save_file(self, json_data):
        av = "av{}".format(json_data["aid"])
        try:
            os.mkdir(av)
        except FileExistsError:
            pass
        with open("{}/{}.json".format(av, av), mode="w", encoding="utf-8") as file:
            file.write(json.dumps(json_data, ensure_ascii=False))
        with open("{}/{}.jpg".format(av, json_data["pic"].split("/")[-1]), mode="wb") as image:
            response = requests.get("https:{}".format(json_data["pic"]), headers=self.headers)
            image.write(response.content)
        print("save completed {}".format(av))

    def spider(self):
        self.get_url()
        self.save_data()


if __name__ == '__main__':
    bss = Bss()
    bss.spider()
