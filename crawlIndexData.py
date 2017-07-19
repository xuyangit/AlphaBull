from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import sys
import json
import datetime
from sqlalchemy import Column, String, Float, SMALLINT, PrimaryKeyConstraint
from sqlUtil import Base, initDB


indexes = {"CPI" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&mkt=19", 1),
           #"GDP" : "http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&mkt=20",
           "PPI" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&mkt=22", 2),
           "PMI" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&mkt=21", 3),
           "房价指数" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&type=GJZB&style=ZGFJ&name=%u5317%u4EAC&code=%u4E0A%u6D77&stat=1&mkt=1", 4),
           "工业增加值增长" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&type=GJZB&style=ZGZB&mkt=0", 5),
           "企业商品价格指数" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&type=GJZB&style=ZGZB&mkt=9", 6),
           "消费者信心指数" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&type=GJZB&style=ZGZB&mkt=4", 7),
           "货币供应量" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/China.ashx?isxml=false&type=GJZB&style=ZGZB&mkt=11", 8),
           "外汇储备" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/goldforexreserve.ashx?mkt=99&stat=17&isxml=false", 9),
           "财政收入" : ("http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/staterevenue.ashx?isxml=false", 10)
        }

class Indexes(Base):
    __tablename__ = "indexes"
    __table_args__ = (
        PrimaryKeyConstraint('time', 'type'),
    )
    time = Column(String)
    type = Column(SMALLINT)
    value = Column(Float)

    def __init__(self, time=None, type=None, value=None):
        self.time = time
        self.type = type
        self.value = value

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




def getHtml(_url):
    req = Request(_url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
    html = urlopen(req).read()
    return html

def getIndexData(session):
    keys = indexes.keys()
    for key in keys:
        jsonStr = str(getHtml(indexes[key][0]), encoding="gb2312")
        obj = json.loads(jsonStr)
        xList = obj["X"].split(",")
        yList = obj["Y"][0].split(",")
        for i, t in enumerate(xList):
            if("/" in t):
                t = datetime.datetime.strptime(t, "%m/%d/%Y").strftime("%Y-%m")
            else:
                t = datetime.datetime.strptime("20" + t, "%Y年%m月").strftime("%Y-%m")
                session.add(Indexes(t, indexes[key][1], yList[i]))
                session.commit()
dbSession = initDB()
print([x.time for x in dbSession.query(Indexes).filter(Indexes.time == '2007-02').all()])
#getIndexData(dbSession)