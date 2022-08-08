import pandas as pd
import re
import jieba
import gensim
from tqdm import tqdm
import numpy as np
from gensim import corpora, models
from gensim.models.word2vec import Word2Vec
import os
##数据过滤
def DataFilter(line):
    res = re.sub('[^\u4e00-\u9fff\！\。\，\？]+','',line)
    return res


def remove_stopwords(word_list,stopwords):
    res = []
    for item in word_list:
        if item not in stopwords:
            res.append(item)
    return res

if __name__ == '__main__':
    #设置话题数量
    topic_num = 5

    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = [item.strip() for item in f.readlines()]

    #选择数据
    print('加载数据')
    df = pd.read_csv('./CSRC/CSRC_Files.csv')
    df2 = df[(df['体裁文种'] == '行政处罚决定') | (df['体裁文种'] == '行政复议') | (df['体裁文种'] == '行政许可批复')]
    df2 = df2[['发文日期', '内容']]
    df2['发文日期'] = pd.DataFrame({'发文日期': [item[:4] for item in df2['发文日期'].tolist()]})
    df2.dropna(inplace=True)
    years = list(set(df2['发文日期'].tolist()))
    for year in years:
        print(year)
        all_data_raw = df2[df2['发文日期'] == year]['内容'].tolist()
        all_data = [remove_stopwords(jieba.lcut(DataFilter(item)), stopwords) for item in all_data_raw]

        # LDA
        # 构建词典与预料
        print('lda')
        dictionary = corpora.Dictionary(all_data)  # 构建 document-term matrix
        corpus = [dictionary.doc2bow(text) for text in all_data]
        lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics=topic_num, id2word=dictionary,
                                                random_state=100, passes=10, workers=3, per_word_topics=30)

        result = {'主题':[],'内容':[]}
        for i in range(topic_num):
            content = lda_model.print_topic(i)
            result['主题'].append('主题'+str(i+1))
            result['内容'].append(str(content))
        pd.DataFrame(result).to_excel('./CSRC主题/'+str(year)+'.xlsx',index=0)
