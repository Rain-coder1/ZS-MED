import json
import requests
from requests.exceptions import RequestException
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import quote


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


def parse_b_tag(tag):
    content = ''
    for child in tag.children:
        if child.name == 'a':
            content += child.b.string.strip() + ' '
        else:
            content += child.string.strip() + ' '
    return content


def parse_a_tag(tag):
    content = ''
    for child in tag.children:
        content += child.string.strip() + ' '
    return content


def parse_one_page(html):
    soup = BeautifulSoup(html,'lxml')

    methods = []

    if soup.find(class_='section steps steps_first sticky') != None:
        methods.append(soup.find(class_='section steps steps_first sticky'))

    methods.extend(soup.find_all(class_='section steps sticky'))

    article_name = soup.find(id='section_0').a.string
    print(article_name)

    event_articles = {}

    description = ''
    description_tag = soup.find(id='mf-section-0').p
    for child in description_tag.children:
    	description += child.string.strip()
      
    for method in methods:
        method_name = method.find(class_='mw-headline').string
        steps = method.find_all(class_='step')
        step_contents = []
        for step in steps:
            # print(step.find(class_="whb"))
            # step_name = step.find(class_="whb").string.strip()
            # step_name = parse_b_tag(step.find(class_="whb"))
            # print(step_name)
            step_content_tags = step.children
            step_content = ''
            for step_content_tag in step_content_tags:
                if step_content_tag.name == None:
                    step_content += step_content_tag.string.strip() + ' '

                elif step_content_tag.name == 'ul':
                    for tag in step_content_tag.find_all(name='li'):
                        for ele in tag.contents:
                            if ele.name == None:
                                step_content += ele.string.strip() + ' '

                elif step_content_tag.name == 'a':
                    step_content += parse_a_tag(step_content_tag)

                elif step_content_tag.name == 'b':
                    step_content += parse_b_tag(step_content_tag)

            # print(step_content)
            step_contents.append(step_content)
        event_articles[method_name] = step_contents

    # print(event_articles)
            
    return article_name,description,event_articles


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def search_wikihow(keyword):
    url = 'https://www.wikihow.com/wikiHowTo?search=' + quote(keyword)
    search_results = get_one_page(url)
    soup = BeautifulSoup(search_results,'lxml')
    result_list_tag = soup.find(id='searchresults_list')
    result_links = result_list_tag.find_all(class_='result_link')

    search_link = []
    

    for link in result_links:
    	search_link.append(link['href'])

    links = []

    for link in search_link[:10]:
        if 'Category' not in link:
            if link not in links:
                links.append(link)
        else:
            html = get_one_page(link)
            new_soup = BeautifulSoup(html,'lxml')
            cat_tags = new_soup.find(class_="cat_grid")
            cnt = 0
            for item in cat_tags.find_all(class_="responsive_thumb"):
                cnt += 1
                if item.a['href'] not in links:
                    links.append(item.a['href'])

    print(len(links))
    print(links)

    # result = {}

    # for link in links:
    #     # print(link)
    #     item = {}
    #     html = get_one_page(link)
    #     print('Now Parse Link: '+link)
    #     name,description,content = parse_one_page(html)
    #     item['description'] = description
    #     item['content'] = content
    #     result[name] = item
    #     time.sleep(1)

    # fw = open('Propose_Marriage.json','w')
    # json.dump(result,fw)


def main(name):
    url = 'https://www.wikihow.com/' + name
    html = get_one_page(url)
    content = parse_one_page(html)
    # print(content)


def test():
	url = 'https://www.wikihow.com/Refuse-a-Marriage-Proposal'
	html = get_one_page(url)
	parse_one_page(html)



if __name__ == '__main__':
    keyword = 'Propose+Marriage'
    search_wikihow(keyword)
    # test()
    # html = get_one_page('https://www.wikihow.com/Propose-to-a-Woman')
    # content = parse_one_page(html)
    

    
