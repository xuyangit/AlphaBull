import tensorflow as tf
import numpy as np
import random
from collections import deque
import datetime
import json
import csv
from snownlp import SnowNLP
import numpy as np

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
            print(line)
            data = [float(x) for x in line.strsplit(" ")]
            print(data)
collectFiles()
#collectFiles()
#for row in trainData:
#    print(row)
# with open("000001.csv") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for line in reader:
#         print(line["涨跌额"])


