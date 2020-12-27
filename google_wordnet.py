import os
import pickle
from first_order_expand import gen_query
from all_events import *
from textblob import TextBlob
from textblob import Word
from nltk.corpus import wordnet as wn


def get_google_concept():
    for event in med_events:
        path = os.path.join('google_articles',event,'google_concepts.pkl')
        google_concepts = pickle.load(open(path,'rb'))
        remained_concept = []
        for concept in google_concepts:
            blob = TextBlob(concept)
            if any(ele[1].startswith('N') for ele in blob.tags):
                remained_concept.append(concept)

        # break
        print('"' + event + '"' + ' : ' + str(remained_concept) + ',')
        # print(remained_concept)
        # print()


# def wordnet():
#     event_querys = gen_query()
#     for event_name in event_querys.keys():
#         print(event_name)
#         print(event_querys[event_name])


if __name__ == "__main__":
    get_google_concept()
    # wordnet()
    # synonyms = []
    # for syn in wordnet.synsets('Dog',pos=wordnet.NOUN):
    #     for lemma in syn.lemmas():
    #         synonyms.append(lemma.name())
    # print(synonyms)

    # dog = wn.synset('dog.n.01')
    # print(dog.hyponyms())