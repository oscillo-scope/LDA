import pandas as pd
from collections import Counter
import gensim
import re
from gensim import corpora, models
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import os
#只保留英文
def remove(line):
    cop = re.compile("[^a-zA-Z ]+")
    return cop.sub("", line)

# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
#词形还原
def cxhy(sentence):
    tokens = word_tokenize(sentence)  # 分词
    tagged_sent = pos_tag(tokens)     # 获取单词词性

    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos)) # 词形还原
    return lemmas_sent

if __name__ == '__main__':
    #设置话题数量
    topic_num = 5
    #设置最低词频
    word_num = 1
    #选择数据
    print('加载数据')
    files = os.listdir('./转化为文本/')
    for file in files:
        print('正在处理：',file)
        with open('./转化为文本/'+file,'r',encoding='utf-8') as f:
            data_ = [ line for line in f.readlines()]
        # 去除标点符号、特殊符号和数字
        data = [remove(item) for item in data_]
        # 小写处理
        data = [str(item).lower() for item in data]
        # 分词
        data = [nltk.word_tokenize(item) for item in data]

        # 删除停用词
        stop_words = stopwords.words("english")
        data_nostopwords = []
        for line in data:
            filtered_sentence = [w for w in line if not w in stop_words and len(w)>1]
            data_nostopwords.append(" ".join(filtered_sentence))
        # 词形还原
        datas = [cxhy(item) for item in data_nostopwords]

        # 构建词典与语料
        dictionary = corpora.Dictionary(datas)  # 构建 document-term matrix
        corpus = [dictionary.doc2bow(text) for text in datas]
        # LDA
        print('lda')
        lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics=topic_num, id2word=dictionary,
                                                random_state=100, passes=10, workers=3, per_word_topics=30)

        result = {'主题':[],'内容':[]}
        for i in range(topic_num):
            content = lda_model.print_topic(i)
            result['主题'].append('主题'+str(i+1))
            result['内容'].append(str(content))
        pd.DataFrame(result).to_excel('./Annual Report on Exchange Arrangements and Exchange Restrictions主题分析/'+file.split('.')[0]+'.xlsx',index=0)
