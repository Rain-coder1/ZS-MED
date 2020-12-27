import os
from textblob import TextBlob
from textblob import Word
import pickle
from all_events import *


def deal_kinetics():
    kinetics_labels = kinetics_classes
    new_labels = []
    new_full_labels = []
    for label in kinetics_labels:
        label = label.split()
        for i in range(len(label)):
            word = label[i]
            word = Word(word)
            word = Word(word.lemmatize())
            word = word.lemmatize('v')
            label[i] = word
        # print(label)
        new_labels.append(label)
        new_full_labels.append(' '.join(label))
    return new_labels,new_full_labels


def deal_query():
    # kinetics_labels = kinetics_classes
    new_google = {}
    for event in med_events:
        query_words = google_concepts[event]
        deal_query = []
        for query in query_words:
            new_word = []
            for word in query.split():
                word = Word(word)
                word = Word(word.lemmatize())
                word = word.lemmatize('v')
                new_word.append(word)
            if len(new_word) > 1:
                new_word = ' '.join(new_word)
            else:
                new_word = new_word[0]
            deal_query.append(new_word)
        new_google[event] = deal_query
    
    return new_google


def get_imagenet_labels():
    path = 'image_net_labels.txt'
    filter_words = ['The','A']
    fr = open(path,'r',encoding='utf-8')
    imagenet_labels = []
    for line in fr.readlines():
        label = line.strip().split()[2:]
        label = [word for word in label if word not in filter_words]
        label = ' '.join(label)
        imagenet_labels.append(label)
        # print(label)
    return imagenet_labels


def deal_imagenet():
    imageNet_labels = get_imagenet_labels()
    new_labels = []
    for i in range(len(imageNet_labels)):
        label = imageNet_labels[i]
        label = label.split()
        for i in range(len(label)):
            word = label[i]
            word = Word(word)
            word = Word(word.lemmatize())
            word = word.lemmatize('v')
            word = word.lower()
            label[i] = word
        # print(label)
        new_labels.append(label)
    return new_labels


def match():
    new_google = deal_query()
    # print(new_google)
    kinetics_labels,kinetics_full = deal_kinetics()
    # kinetics_labels = deal_imagenet()
    new_concept_select = {}
    for event in med_events:
        query = new_google[event]
        # print(query)
        selected_concept = []
        selected_concept_idx = []
        for i in range(len(kinetics_labels)):
            labels = kinetics_labels[i]
            # print(labels)
            # break
            is_in = False
            for word in labels:
                if word in query:
                    selected_concept.append(kinetics_classes[i])
                    # selected_concept.append(imageNet_classes[i])
                    selected_concept_idx.append(i)
                    is_in = True
            if not is_in and kinetics_full[i] in query:
                selected_concept.append(kinetics_classes[i])
                selected_concept_idx.append(i)

        new_concept_select[event] = selected_concept_idx
        print(event)
        print(selected_concept,selected_concept_idx)
    # print(str(new_concept_select))


if __name__ == "__main__":
    # main()
    # deal_kinetics()
    match()
    # deal_imagenet()