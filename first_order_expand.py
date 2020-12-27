import os
import json
from all_events import med_events
from all_events import selected_labels
from textblob import TextBlob
from textblob import Word
import pickle


def gen_query():
    if os.path.exists('event_querys.pkl'):
        return pickle.load(open('event_querys.pkl','rb'))
    event_querys = {}
    for event_name_query in med_events:
        event_name = event_name_query.split('_')
        if 'without' in event_name:
            event_name = event_name[0:event_name.index('without')]
        
        query_words = []
        event_name = ' '.join(event_name)
        
        blob = TextBlob(event_name)
        words = [];tags = []
        for tag in blob.tags:
            tags.append(tag[1])
            if tag[1].startswith('V'):
                word = Word(tag[0].lower()).lemmatize('v')
            else:
                word = Word(tag[0].lower()).lemmatize()
            words.append(word)

        # for idx in range(len(words)):
        #     if tags[idx].startswith('N'):
        #         query_words.append(words[idx])

        word = ''
        for idx in range(len(words)):
            if tags[idx].startswith('N') or tags[idx].startswith('J'):
                if word == '' and tags[idx].startswith('N'):
                    query_words.append(words[idx])
                word += words[idx] + ' '

        if word != '':
            query_words.append(word[:-1])
            query_words.append(word[:-1].split(' ')[-1])
        query_words.append(' '.join(words))
        query_words = list(set(query_words))
        event_querys[event_name_query] = query_words
    
    pickle.dump(event_querys,open('event_querys.pkl','wb'))
    return event_querys
        

if __name__ == '__main__':
    # main()
    query_words = gen_query()
    print(query_words)
    # print(Word('felling').lemmatize('v'))