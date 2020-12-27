from all_events import *
import pickle
import os
import requests
import json
from tqdm import tqdm
import time


def trans(word):
    string = word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    data = {
    'doctype': 'json',
    'type': 'AUTO',
    'i':string
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data,headers=headers)
    # print(r)
    result = r.json()
    translate_result = result['translateResult'][0][0]["tgt"]
    # print(translate_result)
    return translate_result


def translate_image_label():
    path = 'image_net.txt'
    image_labels = []
    fw = open('image_net_labels.txt','a',encoding='utf-8')
    with open(path,'r',encoding='utf-8') as fr:
        for line in fr:
            if line == "\n":
                continue
            split_names = line.strip().split(',')
            labels = split_names[1:]
            idx = split_names[0].split()[0]
            ch_label = split_names[0].split()[-1]
            if int(idx) <= 986:
                continue
            trans_label = trans(ch_label)
            print(ch_label + ' ' + trans_label)
            fw.write(idx + ' ' + ch_label + ' ' + trans_label + '\n')
            # if int(idx) > 500 and int(idx) < 502:
            time.sleep(0.5)
            # image_labels.append([trans_label,labels])

        # pickle.dump(image_labels)


def deal_kinetics():
    print(kinetics_classes)


if __name__ == "__main__":
    # deal_label()
    translate_image_label()
    # deal_kinetics()