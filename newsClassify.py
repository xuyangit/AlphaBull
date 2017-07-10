# _*_coding:utf-8 _*_
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import fasttext
import jieba
import os
if(not os.path.exists("news.bin")):
    classifier = fasttext.supervised("allnews.txt", "news", label_prefix="__label__")
else:
    classifier = fasttext.load_model('news.bin', label_prefix='__label__')
print(classifier.predict(" ".join(jieba.cut("调控效果明显 上半年深圳新房成交均价连续9个月回落"))))
