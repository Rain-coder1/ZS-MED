import json
import requests
from requests.exceptions import RequestException
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
from all_events import med_events
import pickle

import sys
sys.setrecursionlimit(1000000)


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_image_url(event_name,use_cn=False):
    query_item = '+'.join(event_name.split(' '))
    base_url = 'https://www.google.com'
    language = 'en'
    suffix = '&hl=zh-CN'
    url = 'https://www.google.com/search?q={}'.format(query_item)

    if use_cn:
        url += suffix
        language = 'cn'
    html = get_one_page(url)
    soup = BeautifulSoup(html,'lxml')
    select_tag = {'en':'Images','cn':u'图片'}
    image_href = ''
    # fw = open('html.txt','w',encoding='utf-8')
    # fw.write(html)
    for link in soup.find_all('a',class_='hide-focus-ring'):
        # print(link.text)
        if link.text == select_tag[language]:
            image_href = link.get('href')
    
    # print(image_href)
    image_link_href = base_url + image_href
    return image_link_href


def find_google_image(event_name,use_cn=False):
    image_link_href = get_image_url(event_name,use_cn)
    html = get_one_page(image_link_href)
    # print(image_link_href)
    # fw = open('html.txt','w',encoding='utf-8')
    # fw.write(html)
    soup = BeautifulSoup(html,'lxml')

    related_concepts = []

    for tag in soup.find_all('span',class_="hIOe2"):
        # print(tag.string)
        related_concepts.append(tag.string)
    return related_concepts


def parse_one_page(url):
    h_tag = ['h1','h2','h3','h4','h5','h6']
    p_tag = 'p'
    title = {ele:[] for ele in h_tag}
    content = []

    html = get_one_page(url)
    soup = BeautifulSoup(html,'lxml')

    # parse title
    for tag_name in h_tag:
        for tag in soup.find_all(tag_name):
            text = tag.text.strip()
            title[tag_name].append(text)

    for tag in soup.find_all('p'):
        text = tag.text.strip()
        content.append(text)

    return title, content


def crawl_google_atricles(event_name,number = 50,use_cn = False):
    # pass
    print('Crawing pages of event: [{}]'.format(event_name))
    url = get_image_url(event_name,use_cn)
    html = get_one_page(url)
    soup = BeautifulSoup(html,'lxml')

    parse_links = []
    result_link_class = "VFACy kGQAp sMi44c lNHeqe WGvvNb"

    for tag in soup.find_all('a',class_=result_link_class):
        page_link = tag.get('href')
        if page_link != None:
            parse_links.append(page_link)
            if len(parse_links) >= number:
                break

    articles = {}

    for idx,page_link in enumerate(parse_links):
        print('{0}: Now paring link {1}'.format(idx,page_link))
        try:
            now_time = time.time()
            title, content = parse_one_page(page_link)
            print('Finished')
            articles[page_link] = [title,content]
            time.sleep(2)
        except:
            print('Parse Error')

    return articles


def show_article(articles):
    for key in articles.keys():
        article = articles[key]
        title, content = article[0], article[1]
        print(title)


def main():
    save_dir = 'google_articles'
    for event in med_events:
        events_split = event.split('_')
        event_name = ' '.join(events_split)
        print('Now deal with event : {}'.format(event_name))
        event_dir = event
        event_google_file = event_dir + '_google_article.json'
        
        event_result_dir = os.path.join(save_dir,event_dir)
        # print(event_result_dir)
        if not os.path.exists(event_result_dir):
            os.makedirs(event_result_dir)

        related_concepts = find_google_image(event_name)
        print('related_concepts is : ',related_concepts)

        if os.path.exists(os.path.join(event_result_dir,event_google_file)):
            articles = json.load(open(os.path.join(event_result_dir,event_google_file)))
        else:
            related_concepts = find_google_image(event_name)
            print('related_concepts is : ',related_concepts)
            pickle.dump(related_concepts,open(os.path.join(event_result_dir,'google_concepts.pkl'),'wb'))
            articles = crawl_google_atricles(event_name)
            json.dump(articles,open(os.path.join(event_result_dir,event_google_file),'w'))
        


def gen_google_first_order_concept():
    save_dir = 'google_articles'
    for event in med_events:
        event_result_dir = os.path.join(save_dir,event)
        related_concepts = pickle.load(open(os.path.join(event_result_dir,'google_concepts.pkl'),'rb'))
        print(event)
        print(related_concepts)


if __name__ == '__main__':
    # main()
    gen_google_first_order_concept()

