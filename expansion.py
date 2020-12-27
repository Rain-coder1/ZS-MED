import os
import pickle
from all_events import *
import json
from textblob import TextBlob
from textblob import Word
import math


def gen_word_cnts():
    for event in med_events:
        print(event)
        path = os.path.join('google_articles',event,event+'_google_article.json')
        articles = json.load(open(path,'r'))
        title_text = ""
        content_text = ""
        for key in articles.keys():
            title, content = (articles[key][0],articles[key][1])
            for title_key in title.keys():
                string_blob = TextBlob(' '.join(title[title_key]))
                title_text += ' '.join([Word(string_blob.tags[i][0]).lemmatize() for i in range(len(string_blob.tags)) if string_blob.tags[i][1].startswith('N')])
                # print(title_text)
                # title_text += ' '.join(TextBlob().words.lemmatize())

            title_text += ' '
            string_blob = TextBlob(' '.join(content))
            title_text += ' '.join([Word(string_blob.tags[i][0]).lemmatize() for i in range(len(string_blob.tags)) if string_blob.tags[i][1].startswith('N')])

        path = os.path.join('wikihow_articles',event+'.json')
        if os.path.exists(path):
            articles = json.load(open(path,'r'))

            for key in articles.keys():
                des, content = (articles[key]["description"],articles[key]["content"])
                string_blob = TextBlob(des)
                title_text += ' '.join([Word(string_blob.tags[i][0]).lemmatize() for i in range(len(string_blob.tags)) if string_blob.tags[i][1].startswith('N')])
                for content_key in content.keys():
                    string_blob = TextBlob(' '.join(content[content_key]))
                    title_text += ' '.join([Word(string_blob.tags[i][0]).lemmatize() for i in range(len(string_blob.tags)) if string_blob.tags[i][1].startswith('N')])
                    string_blob = TextBlob(content_key)
                    title_text += ' '.join([Word(string_blob.tags[i][0]).lemmatize() for i in range(len(string_blob.tags)) if string_blob.tags[i][1].startswith('N')])

        blob = TextBlob(title_text)
        # print(type(blob.word_counts))
        word_counts = blob.word_counts
        # print(word_counts['bike'])
        # sorted_word_counts = sorted(blob.word_counts.items(),key=lambda x: x[1],reverse=True)
        path = os.path.join('word_counts',event+'_words_cnt.pkl')
        pickle.dump(word_counts,open(path,'wb'))
        

def query_word_cnt(event,words):
    path = os.path.join('word_counts',event+'_words_cnt.pkl')
    word_cnts = pickle.load(open(path,'rb'))
    max_cnts = 0
    for word in words:
        cnt = word_cnts.get(word,0)
        max_cnts = max(max_cnts,cnt)
    return cnt


def normalize(word_cnt):
    # frac
    # total_feq = sum(word_cnt.values())
    # normal_freq = word_cnt.copy()
    # assert total_feq > 0
    # for key,item in normal_freq.items():
    #     normal_freq[key] = item / total_feq
    # return normal_freq

    # softmax
    eps = 1e-8
    total_feq = sum([math.log2(val+1) for val in word_cnt.values()])
    normal_freq = word_cnt.copy()
    assert total_feq >= 0,print(word_cnt)
    for key,item in normal_freq.items():
        normal_freq[key] = (math.log2(item+1) / (total_feq + eps)) * 100
    return normal_freq


def cal_final_score():
    for event in med_events:
        print(event)
        path = os.path.join('relatedness',event+'_rel.pkl')
        relatedness = pickle.load(open(path,'rb'))
        
        # print('"' + event + '"' + " : " + str(list(relatedness.keys())) + ",")
        event_score = {}
        for key in event_query[event]:
            items = relatedness[key]
            word_cnts = {}
            for ele in items:
                query = ele[0]
                rel = ele[1]
                if rel > 0:
                    query = TextBlob(query).words.lemmatize()
                    frequency = query_word_cnt(event,query)
                    word_cnts[ele] = frequency
        
            normal_freq = normalize(word_cnts)
            final_score = {}
            for n_key in normal_freq.keys():
                final_score[n_key[0]] = n_key[1] * (1 + normal_freq[n_key])
            # print(final_score)
            sorted_score = sorted(final_score.items(),key = lambda x: x[1],reverse=True)
            event_score[key] = sorted_score
            # print(sorted_score)
            # print()
        path = os.path.join('final_score',event+"_score.pkl")
        pickle.dump(event_score,open(path,'wb'))


if __name__ == "__main__":
    # gen_word_cnts()
    cal_final_score()