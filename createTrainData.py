import json
import jieba
files = ["companynews.txt", "cpinews.txt", "estatenews.txt", "gdpnews.txt", "industrynews.txt", "marketnews.txt",
         "ppinews.txt", "rmbnews.txt"]
def collectFiles():
    with open("allnews.txt", mode="w", encoding="utf-8") as allf:
        for file in files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    news = json.loads(line)
                    content = " ".join(jieba.cut(news["content"]))
                    allf.write(content + " __label__" + news["type"] + "\n")
collectFiles()
