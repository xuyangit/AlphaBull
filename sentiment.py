from snownlp import SnowNLP
import json
with open("labeled.txt", encoding="utf-8") as f:
    for line in f:
        news = json.loads(line)
        s = SnowNLP(news["content"])
        print(news["content"], s.sentiments, news["type"])