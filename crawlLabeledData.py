#coding:utf-8
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import sys
import json
import datetime
import time
def getHtml(_url):
    req = Request(_url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
    html = urlopen(req).read()
    return html
def getLabeledData(seq):
    # crawl labeled data from http://stock.10jqka.com.cn/thsgd/realtimenews.js?_=
    url = "http://stock.10jqka.com.cn/thsgd/realtimenews.js?_="
    page = str(getHtml(url), encoding="gbk")
    jsonStr = '{"item":' + page[page.index("item") + 5:-91]
    newsList = json.loads(jsonStr)["item"]
    newsMap = {"1":"positive", "2":"negative", "3":"neutral"}
    tpSeq = []
    with open("sentimentlabeled.txt", mode="a", encoding="utf-8") as f:
        for news in newsList:
            tpSeq.append(news["seq"])
            if(news["seq"] in seq or news["nature"] == ""):
                continue
            newsType = newsMap[news['nature']]
            content = news["title"]
            newsDate = datetime.datetime.strptime(news["pubDate"], "%Y/%m/%d %H:%M").strftime("%Y-%m-%d %H:%M")
            data = {
                'time': newsDate,
                'content': content,
                'type': newsType
            }
            json.dump(data, f, ensure_ascii=False, sort_keys=False)
            f.write("\n")
    return tpSeq
newsSeq = []
while True:
    newsSeq = getLabeledData(newsSeq)
    time.sleep(120)