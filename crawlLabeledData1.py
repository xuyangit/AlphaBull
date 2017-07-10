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
def getLabeledData():
    # crawl labeled data from http://comment.10jqka.com.cn/api/realtime.php?block=getnews&page=3&jsoncallback=jQuery18308917795699947166_1499568509621&_=1499568509974
    urlHolder = "http://comment.10jqka.com.cn/api/realtime.php?block=getnews&page={}&jsoncallback=jQuery18308917795699947166_1499568509621&_=1499568509974"
    newsMap = {"1":"positive", "2":"negative", "3":"neutral"}
    with open("labeled.txt", mode="w", encoding="utf-8") as f:
        for i in range(1, 20):
            url = urlHolder.format(i)
            page = str(getHtml(url), encoding="utf-8")
            newsList = json.loads(page[41:-1])
            for news in newsList:
                if(news["nature"] == ""):
                    continue
                newsType = newsMap[news['nature']]
                content = news["title"]
                data = {
                    'content': content,
                    'type': newsType
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
getLabeledData()