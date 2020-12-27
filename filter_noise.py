import json
import nltk

from textblob import TextBlob
from textblob import Word

import os
import pickle

_wordnet = nltk.corpus.wordnet


def de_duplicate(info_list,filter_words):
    info_num = len(info_list)
    single_info = set([])
    info_cnt = {}
    # print(info_num)
    for idx in range(info_num):
        info = info_list[idx]
        blod = TextBlob(info)
        new_words = []
        word_tags = {}
        for tag in blod.tags:
            word_tags[tag[0]] = tag[1]
        # print(word_tags)
        for word in blod.words:
            if 'V' in word_tags[str(word)]:
                new_word = word.lemmatize('v')
                # print(word,word_tags[word],new_word)
            else:
                new_word = word.lemmatize()
            new_word = new_word.lower()
            new_words.append(new_word)

        info = ' '.join(new_words)
        single_info.add(info)
        info_cnt[info] = info_cnt.get(info,0) + 1

    return list(single_info), info_cnt


def main():
    output_dir = 'highorder_info'
    # event_name = 'Birthday_party'
    event_name = 'Playing_fetch'
    filter_words = ['ball','fetch','frisbee']   # low-order expansion
    high_order_info = pickle.load(open(os.path.join(output_dir,event_name+'.pkl'),'rb'))
    deduped_high_info, high_info_num = de_duplicate(high_order_info,filter_words)
    # print(len(deduped_high_info))
    for info in deduped_high_info:
        # print(info)
        print(info,high_info_num[info])
    # print('\n'.join(deduped_high_info))


if __name__ == '__main__':
    main()