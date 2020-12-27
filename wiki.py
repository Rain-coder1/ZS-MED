from bs4 import BeautifulSoup
import requests
import time


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


def parse_wiki(html):
    soup = BeautifulSoup(html,'lxml')
    p_tags = soup.find_all(name='p')

    cnt = 0

    for p_tag in p_tags:
        content = ''
        for child in p_tag.children:
            if child.name != 'sup':
                content += child.string
        print(content)


if __name__ == '__main__':
    keyword = 'Marriage_proposal'
    html = get_one_page('https://en.wikipedia.org/wiki/'+keyword)
    parse_wiki(html)