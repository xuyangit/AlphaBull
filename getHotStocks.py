import requests
import json
import datetime
import csv
import time
from sqlalchemy import Column, String, Float, Integer, PrimaryKeyConstraint, Date, desc
from sqlUtil import Base, initDB

# 获取雪球网的总评论数目和关注数目以及其自身的热股榜（作为参考）
class XueqiuHotness(Base):
    __tablename__ ="xueqiuhotness"
    __table_args__ = (
        PrimaryKeyConstraint('time', 'code'),
    )
    time = Column(Date)
    code = Column(String)
    name = Column(String)
    count = Column(Integer)
    def __init__(self, time=None, code=None, name=None, count=None):
        self.time = time
        self.code = code
        self.name = name
        self.count = count

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class AllHotness(Base):
    __tablename__ = "allhotness"
    __table_args__ = (
        PrimaryKeyConstraint('time', 'code'),
    )
    time = Column(Date)
    code = Column(String)
    name = Column(String)
    tweet = Column(Integer)
    follow = Column(Integer)

    def __init__(self, time=None, code=None, name=None, tweet=None, follow=None):
        self.time = time
        self.code = code
        self.name = name
        self.tweet = tweet
        self.follow = follow

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DayHotness(Base):
    __tablename__ = "dayhotness"
    __table_args__ = (
        PrimaryKeyConstraint('time', 'code'),
    )
    time = Column(Date)
    code = Column(String)
    name = Column(String)
    tweet = Column(Integer)
    follow = Column(Integer)

    def __init__(self, time=None, code=None, name=None, tweet=None, follow=None):
        self.time = time
        self.code = code
        self.name = name
        self.tweet = tweet
        self.follow = follow

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) ' \
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'


r = requests.get('https://xueqiu.com/', headers={'User-Agent': agent})
token = str(r.cookies['xq_a_token'])
cook_token = 'xq_a_token={token}'.format(token=token)
today = datetime.datetime.today().date()
dbSession = initDB()
def getCommentAndFollow():
    url = 'https://xueqiu.com/stock/screener/screen.json?' \
      'category=SH&orderby=symbol&order=desc&' \
      'page={page}&tweet=0_{max_t}&follow=0_{max_f}'
    timeRes = dbSession.query(AllHotness.time).distinct().order_by(desc(AllHotness.time)).all()
    recentDay = None
    if (timeRes):
        recentDay = timeRes[0].time
    for i in range(1, 112):
        xueqiu = url.format(page=i, max_t=10000000, max_f=10000000)
        data = requests.get(xueqiu, headers={'User-Agent': agent, 'Cookie': cook_token})
        stock_json = json.loads(data.text, encoding="utf-8")['list']
        for stock in stock_json:
            try:
                if(dbSession.query(AllHotness).filter(AllHotness.time == today, AllHotness.code == str(stock['symbol'])[2:]).count() == 0):
                    if(recentDay):
                        res = dbSession.query(AllHotness).filter(AllHotness.time == recentDay, AllHotness.code == str(stock['symbol'])[2:]).all()
                        if(res):
                            dbSession.add(DayHotness(today, str(stock['symbol'])[2:], stock['name'],
                                         int(stock['tweet'] - res[0].tweet),
                                         int(stock['follow'] - res[0].follow))
                            )

                    dbSession.add(AllHotness(today, str(stock['symbol'])[2:], stock['name'], int(stock['tweet']),
                                             int(stock['follow'])))
                    dbSession.commit()
                else:
                    tpRes = dbSession.query(AllHotness).filter(AllHotness.time == today, AllHotness.code == str(stock['symbol'])[2:]).first()
                    dayRes = dbSession.query(DayHotness).filter(DayHotness.time == today, DayHotness.code == str(stock['symbol'])[2:]).all()
                    if(dayRes):
                        dayRes[0].tweet += (int(stock['tweet']) - tpRes.tweet)
                        dayRes[0].follow += (int(stock['follow']) - tpRes.follow)
                    tpRes.tweet = int(stock['tweet'])
                    tpRes.follow = int(stock['follow'])
                    dbSession.commit()
            except Exception as e:
                print(str(e))
                print(str(stock['symbol'])[2:], stock['name'], int(stock['tweet']), int(stock['follow']))
                return
def getHotnessOfXueqiu():
    hotPerDay = "https://xueqiu.com/stock/rank.json?size=20&_type=12&type=22"
    data = requests.get(hotPerDay, headers={'User-Agent': agent, 'Cookie': cook_token}).text
    stocks = json.loads(data)["ranks"]
    dbSession.query(XueqiuHotness).filter(XueqiuHotness.time == today).delete()
    dbSession.commit()
    for stock in stocks:
        dbSession.add(XueqiuHotness(today, str(stock['symbol'])[2:], stock['name'], int(stock['count'])))
        dbSession.commit()
#针对14号数据融合，后面不用再调用了
def insertHisdata():
    with open("./crawldata/2017-07-14.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        day = datetime.date(2017, 7, 14)
        for line in reader:
            if (dbSession.query(AllHotness).filter(AllHotness.time == day, AllHotness.code == line['code']).count() == 0):
                res = dbSession.query(AllHotness).filter(AllHotness.code == line['code']).all()
                if(res):
                    dbSession.add(DayHotness(today, line['code'], line['name'],
                                             res[0].tweet - int(float(line['tweet'])),
                                             res[0].follow - int(float(line['follow'])))
                                  )
                    dbSession.commit()
                dbSession.add(AllHotness(day, line['code'], line['name'], int(float(line['tweet'])), int(float(line['follow']))))
                dbSession.commit()
#返回按照新增评论数目，关注数目
def getHotStocks():
    #返回雪球网的当前热榜
    xueqiuRes = dbSession.query(XueqiuHotness).all()
    #返回新增评论和关注数的topK结果
    tweetRes = dbSession.query(DayHotness).order_by(desc(DayHotness.tweet)).limit(20).all()
    followRes = dbSession.query(DayHotness).order_by(desc(DayHotness.follow)).limit(20).all()
    return ([x.as_dict() for x in xueqiuRes],
            [x.as_dict() for x in tweetRes],
            [x.as_dict() for x in followRes],
    )
#insertHisdata()
while(True):
    print("Update Data!")
    today = datetime.datetime.today().date()
    getCommentAndFollow()
    getHotnessOfXueqiu()
    print("Update Ending!")
    time.sleep(3600)




