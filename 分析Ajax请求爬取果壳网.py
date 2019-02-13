__author__ = 'Administrator'
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from urllib.parse import urlencode
def get_index(offset):
    base_url='https://www.guokr.com/apis/minisite/article.json?'
    data={
        'retrieve_type':'by_subject',
        'limit':'20',
        'offset':offset
        }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    proxiex={'https':'https://203.86.26.9:3128'}
    parse=urlencode(data,encoding='utf-8')
    url=base_url+parse
    try:
        resp=requests.get(url,headers=headers,proxies=proxiex)
        soup=BeautifulSoup(resp.text,'lxml')
        print(resp.status_code)
        if resp.status_code==200:
            return resp.text
        return None
        if resp.status_code==403:
            print('403')
    except ConnectionError:
        print('error')
        return None

import json
#解析json
def parse_json(text):
    try:
        result=json.loads(text)
        if result:
            for i in result.get('result'):
                #print(i)
                print(i.get('url'))
                yield i.get('url')
    except:pass
def parse_page(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        content = soup.find('div', class_="content")
        title = content.find('h1', id="articleTitle").get_text()
        author = content.find('div', class_="content-th-info").find('a').get_text()
        article_content = content.find('div', class_="document").find_all('p')
        all_p = [i.get_text() for i in article_content if not i.find('img') and not i.find('a')]
        article = '\n'.join(all_p)
        # print(title,'\n',author,'\n',article)
        data = {
            'title': title,
            'author': author,
            'article': article
        }
        return data
    except:
        pass
import pymongo
from config import *

client = pymongo.MongoClient('localhost', 27017)
db = client['guoke']

def save_database(data):
    if db['guoke'].insert(data):
        print('Save to Database successful', data)
        return True
    return False
from multiprocessing import Pool

# 定义一个主函数
def main(offset):
    text = get_index(offset)
    all_url = parse_json(text)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    proxiex={'https':'https://203.86.26.9:3128'}
    for url in all_url:

        resp = requests.get(url,headers=headers,proxies=proxiex)
        data = parse_page(resp)
        if data:
            print(data)
            save_database(data)
        else:
            print('123')

if __name__ == '__main__':
    pool = Pool()
    offsets = ([0] + [i*20+18 for i in range(500)])
    pool.map(main, offsets)
    pool.close()
    pool.join()