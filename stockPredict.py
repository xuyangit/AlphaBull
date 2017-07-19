import datetime
import json
import csv
from snownlp import SnowNLP
import numpy as np
from rnn import RNN
from sklearn.metrics import mean_squared_error
newsType = 5
files = ["marketnews.txt", "companynews.txt", "cpinews.txt", "estatenews.txt", "gdpnews.txt", "industrynews.txt",
         "ppinews.txt", "rmbnews.txt"]
trainData = np.zeros((731, 4))
countData = np.zeros((731, 4))
startDate = datetime.date(2015, 1, 1)
newsMap = {"companynews" : 0, "marketnews" : 1, "industrynews" : 2, "economynews" : 3}
def collectFiles():
    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                try:
                    news = json.loads(line)
                    newsDate = datetime.datetime.strptime(news["time"], "%Y-%m-%d %H:%M")
                    timeDelta = (newsDate.date() - startDate).days
                    if(timeDelta < 0 or timeDelta >= 731):
                        continue
                    record = trainData[timeDelta]
                    countRecord = countData[timeDelta]
                    s = SnowNLP(news["content"])
                    index = newsMap[news["type"]]
                    record[index] += s.sentiments
                    countRecord[index] += 1
                except Exception:
                    continue
    with open("traindata.txt", mode="w") as f:
        for i in range(731):
            for j in range(4):
                if(countData[i][j] != 0):
                    trainData[i][j] = trainData[i][j] / countData[i][j]
                f.write(str(trainData[i][j]) + " ")
            f.write("\n")
def readTraindata():
    with open("traindata.txt") as f:
        lines = f.readlines()
        for i in range(731):
            line = lines[i][1:-2]
            data = [float(x) for x in line.split(" ")]
            trainData[i] = data
dayLen = 3
allDataX = []
allDataY = []
readTraindata()
with open("000001.csv", encoding="gbk") as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        day = datetime.datetime.strptime(line["日期"], "%Y/%m/%d").date()
        timeDelta = (day - startDate).days
        if(timeDelta >= dayLen and timeDelta < 731):
            #allDataX.append(np.array([trainData[timeDelta - i] for i in range(dayLen)]).flatten())
            allDataX.append(trainData[timeDelta - 1])
            allDataY.append(float(line["涨跌额"]))
allDataX = np.array(allDataX)
allDataX = np.reshape(allDataX, (allDataX.shape[0], 1, allDataX.shape[1]))
#np.reshape(allDataX, ())
trainDataX = allDataX[:-80]
trainDataY = allDataY[:-80]
testDataX = allDataX[-80:]
testDataY = allDataY[-80:]
rnn = RNN([4, 10, 10, 1])
rnn.fit(trainDataX, trainDataY, epochs=10000)
p = rnn.predict(testDataX)
count = 0
for i in range(len(p)):
    print(testDataY[i], p[i])
    if(testDataY[i] * p[i] > 0):
        count += 1
print(count, len(p), "correct rate: ", count / len(p))
print(mean_squared_error(testDataY, p))
