#coding:utf-8
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import sys
import json
import datetime

def getHtml(_url):
    req = Request(_url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
    html = urlopen(req).read()
    return html
def getPoliticalNews():
    return
def getPpiNews():
    # crawl ppi news from http://news.fx678.com/news/keywords/cncpi.shtml
    urlHolder = "http://news.fx678.com/news/keywords/cnppi{}.shtml"
    urlList = [urlHolder.format(i) for i in range(2, 8)]
    urlList.append("http://news.fx678.com/news/keywords/cnppi.shtml")
    with open("ppinews.txt", mode="w", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            uList = soup.find("ul", id="analysis_ul").find_all('li')
            for l in uList:
                tpDate = datetime.datetime.strptime(l.find("div", class_="clock_touzi").string[:17], "%Y年%m月%d日 %H:%M")
                newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                contentUrl = "http://news.fx678.com" + l.find("h1").find("a")['href']
                contentPage = getHtml(contentUrl)
                contentSoup = BeautifulSoup(contentPage, "html.parser", from_encoding="utf-8")
                content = ""
                try:
                    content = contentSoup.find("div", class_="new_inter_left_position_title").string
                except Exception:
                    content = contentSoup.find("h1", class_="new_inter_left_position_title").string
                if (content[-1] == '；'):
                    content = content[:-1]
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'ppinews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getCpiNews():
    # crawl cpi news from http://news.fx678.com/news/keywords/cncpi.shtml
    urlHolder = "http://news.fx678.com/news/keywords/cncpi{}.shtml"
    urlList = [urlHolder.format(i) for i in range(2, 11)]
    urlList.append("http://news.fx678.com/news/keywords/cncpi.shtml")
    with open("cpinews.txt", mode="w", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            uList = soup.find("ul", id="analysis_ul").find_all('li')
            for l in uList:
                tpDate = datetime.datetime.strptime(l.find("div", class_="clock_touzi").string[:17], "%Y年%m月%d日 %H:%M")
                newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                contentUrl = "http://news.fx678.com" + l.find("h1").find("a")['href']
                contentPage = getHtml(contentUrl)
                contentSoup = BeautifulSoup(contentPage, "html.parser", from_encoding="utf-8")
                content = ""
                try:
                    content = contentSoup.find("div", class_="new_inter_left_position_title").string
                except Exception:
                    content = contentSoup.find("h1", class_="new_inter_left_position_title").string
                if (content[-1] == '；'):
                    content = content[:-1]
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'cpinews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")

def getExchangeNews():
    #crawl exchange news from http://news.fx678.com/news/keywords/whcb.shtml
    urlList = ["http://news.fx678.com/news/keywords/whcb.shtml", "http://news.fx678.com/news/keywords/whcb2.shtml"]
    with open("rmbnews.txt", mode="a", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            uList = soup.find("ul", id="analysis_ul").find_all('li')
            for l in uList:
                tpDate = datetime.datetime.strptime(l.find("div", class_="clock_touzi").string[:17], "%Y年%m月%d日 %H:%M")
                newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                contentUrl = "http://news.fx678.com" + l.find("h1").find("a")['href']
                contentPage = getHtml(contentUrl)
                contentSoup = BeautifulSoup(contentPage, "html.parser", from_encoding="utf-8")
                content = ""
                try:
                    content = contentSoup.find("div", class_="new_inter_left_position_title").string
                except Exception:
                    content = contentSoup.find("h1", class_="new_inter_left_position_title").string
                if (content[-1] == '；'):
                    content = content[:-1]
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'rmbnews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getGdpNews():
    #crawl gdp news from http://news.fx678.com/news/keywords/zggdp.shtml
    urlHolder = "http://news.fx678.com/news/keywords/zggdp{}.shtml"
    urlList = [urlHolder.format(i) for i in range(2, 11)]
    urlList.append("http://news.fx678.com/news/keywords/zggdp.shtml")
    with open("gdpnews.txt", mode="w", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            uList = soup.find("ul", id="analysis_ul").find_all('li')
            for l in uList:
                tpDate = datetime.datetime.strptime(l.find("div", class_="clock_touzi").string[:17], "%Y年%m月%d日 %H:%M")
                newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                contentUrl = "http://news.fx678.com" + l.find("h1").find("a")['href']
                contentPage = getHtml(contentUrl)
                contentSoup = BeautifulSoup(contentPage, "html.parser", from_encoding="utf-8")
                content = ""
                try:
                    content = contentSoup.find("div", class_="new_inter_left_position_title").string
                except Exception:
                    content = contentSoup.find("h1", class_="new_inter_left_position_title").string
                if (content[-1] == '；'):
                    content = content[:-1]
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'gdpnews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getRmbNews1():
    #crawl rmb news from http://news.fx678.com/news/keywords/cny2.shtml
    urlHolder = "http://news.fx678.com/news/keywords/cny{}.shtml"
    urlList = [urlHolder.format(i) for i in range(2, 11)]
    urlList.append("http://news.fx678.com/news/keywords/cny.shtml")
    with open("rmbnews.txt", mode="a", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            uList = soup.find("ul", id="analysis_ul").find_all('li')
            for l in uList:
                tpDate = datetime.datetime.strptime(l.find("div", class_="clock_touzi").string[:17], "%Y年%m月%d日 %H:%M")
                newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                contentUrl = "http://news.fx678.com" + l.find("h1").find("a")['href']
                contentPage = getHtml(contentUrl)
                contentSoup = BeautifulSoup(contentPage, "html.parser", from_encoding="utf-8")
                content = contentSoup.find("h1", class_="new_inter_left_position_title").string
                if(content[-1] == '；'):
                    content = content[:-1]
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'rmbnews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getRmbNews():
    #crawl rmb news from http://money.163.com/baike/renminbihuilv/
    urlHolder = "http://money.163.com/baike/renminbihuilv/0{}/"
    urlList = [urlHolder.format(i) for i in range(2, 10)]
    urlList.append("http://money.163.com/baike/renminbihuilv/")
    urlList.append("http://money.163.com/baike/renminbihuilv/10")
    with open("rmbnews.txt", mode="w", encoding="utf-8") as f:
        for url in urlList:
            page = getHtml(url)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            ulist = soup.find_all("div", class_="list_item")
            for l in ulist:
                newsDate = l.span.string[5:]
                content = l.find("a").string
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'rmbnews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")

def getMarketNews():
    #crawl market news from http://open.tool.hexun.com/, this is a convenient json interface
    urlHolder = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100235808&s=30&cp={}&priority=0&callback="
    with open("marketnews.txt", mode="w", encoding="utf-8") as f:
        for i in range(1, 1300):
            tmpUrl = urlHolder.format(i)
            page = str(getHtml(tmpUrl), encoding='gbk')
            results = json.loads(page)['result']
            for result in results:
                newsDate = result['entityurl'][23:33] + " " + result['entitytime'][-5:]
                content = result['title']
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'marketnews',
                    'subtype': 'marketnews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")



def getEstateNews():
    # crawl estate news from http://www.zhicheng.com
    urlHolder = "http://www.zhicheng.com/fc/index_{}.html"
    with open("estatenews.txt", mode="w", encoding="utf-8") as f:
        for i in range(2, 148):
            tmpUrl = urlHolder.format(i)
            page = getHtml(tmpUrl)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            ulist = soup.find_all("div", class_="fonav_bd")
            for l in ulist:
                newsDate = l.find("span").string
                content = l.find("a").string
                if (newsDate[0] != '2' and newsDate[0] != '今'):
                    tpDate = datetime.datetime.strptime("2017年" + newsDate, "%Y年%m月%d日 %H:%M")
                    newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'economynews',
                    'subtype': 'estatenews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getIndustryNews():
    #crawl industry news from http://www.zhicheng.com
    urlHolder = "http://www.zhicheng.com/hgcy/index_{}.html"
    with open("industrynews.txt", mode="w", encoding="utf-8") as f:
        for i in range(2, 203):
            tmpUrl = urlHolder.format(i)
            page = getHtml(tmpUrl)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            ulist = soup.find_all("div", class_="fonav_bd")
            for l in ulist:
                newsDate = l.find("span").string
                content = l.find("a").string
                if(newsDate[0] != '2' and newsDate[0] != '今'):
                    tpDate = datetime.datetime.strptime("2017年" + newsDate, "%Y年%m月%d日 %H:%M")
                    newsDate = tpDate.strftime("%Y-%m-%d %H:%M")
                data = {
                    'time': newsDate,
                    'content': content,
                    'type': 'industrynews',
                    'subtype': 'industrynews'
                }
                json.dump(data, f, ensure_ascii=False, sort_keys=False)
                f.write("\n")
def getCompanyNews():
    #crawl company news from http://www.southmoney.com, we can get all by filling blank in rootUrl
    rootUrl = "http://www.southmoney.com"
    urlHolder = "http://www.southmoney.com/caijing/gongsixinwen/list_45_{}.html"
    with open("companynews.txt", mode="w", encoding="utf-8") as f:
        for i in range(1, 298):
            tmpUrl = urlHolder.format(i)
            page = getHtml(tmpUrl)
            soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
            ulist = soup.find("ul", class_="newslist").find_all('li')
            for l in ulist:
                try:
                    #we jump to detail url to get the date with hours and minutes
                    detailUrl = rootUrl + l.a['href']
                    detailSoup = BeautifulSoup(getHtml(detailUrl), "html.parser", from_encoding="utf-8")
                    newsDate = ""
                    try:
                        newsDate = detailSoup.find("p", class_="artDate").contents[0][:16]
                    except Exception:
                        newsDate = detailSoup.find("span", id="articleTime").contents[0][:16]
                    content = l.a.string
                    data = {
                        'time' : newsDate,
                        'content' : content,
                        'type': 'companynews',
                        'subtype': 'companynews'
                    }
                    json.dump(data, f, ensure_ascii=False, sort_keys=False)
                    f.write("\n")
                except Exception:
                    continue
if __name__=="__main__":
    getPpiNews()
