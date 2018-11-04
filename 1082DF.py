#coding=utf-8
import re, os
import requests
import time, threading
import ssl, random
from bs4 import BeautifulSoup

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
index = random.randint(0, 9)
user_agent = user_agents[index]
headers = {'User_agent': user_agent}

page_urls=['https://www.1082df.com/pic/6/index_{pn}.html'.format(pn=pn) for pn in range(2,62)]
ssl._create_default_https_context=ssl._create_unverified_context()
# post_urls=[]
img_num=0

def get_post_urls(page_url):
    post_urls=[]
    html=requests.get(page_url, headers=headers).text
    tag=BeautifulSoup(html, 'lxml').find('div', class_='channel').find('ul').find_all('a')
    result = re.findall(r"(?<=href=)\S+", str(tag))
    post_url_index=[url.replace('"', "") for url in result]
    base_url='https://www.1082df.com'
    urls=map(lambda x:base_url+x , post_url_index)
    post_urls.extend(urls)
    return post_urls

def save_img(img_url, save_path):
    global img_num
    try:
        time.sleep(0.10)
        img = requests.get(img_url, headers=headers, timeout=10)
        img_name = r"F:\Study-Work\CrawThing\1052DF_Dongman\pic_cnt_%d.jpg"%img_num
        with open(img_name, 'ab') as f:
            f.write(img.content)
            print(img_name)
        img_num+=1
    except Exception as e:
        print(e)
    pass

def get_post_imgs(url):
    urls=[]
    save_path = r"F:\Study-Work\CrawThing\1052DF_Dongman"
    html=requests.get(url, headers=headers).text
    tag=BeautifulSoup(html, 'lxml').find('div', class_='content').find_all('img')
    results=re.findall(r"(?<=src=)\S+", str(tag))
    if results :
        urls= [url.replace('"', "").replace('/>,', '').replace('/>]', '') for url in results]
    print('img urls:', end='')
    print(urls)
    for url in urls:
        save_img(url, save_path)


def StartRun():
    for page in range(1, 62):
        if page==1:
            pageurl='https://www.1082df.com/pic/6/index.html'
        else:
            pageurl=page_urls[page-2]
        print('pageurl is :%s'%pageurl)
        urls=get_post_urls(pageurl)
        print('get_post_urls:', end='')
        print(urls)
        for url in urls:
            get_post_imgs(url)

if __name__=='__main__':
    StartRun()
    # print(page_urls)
    pass