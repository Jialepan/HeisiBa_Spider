#coding=utf-8
import re, os
import requests
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

ssl._create_default_https_context=ssl._create_unverified_context()
page_url='http://tieba.baidu.com/f/fdir?fd=%C7%E9%B8%D0&sd=%C3%C0%C9%AB&pn=1'

html=requests.get(page_url, headers=headers).text
tagurls=BeautifulSoup(html, 'lxml').find_all('td')
tags=[]
for tag in tagurls:
    if 'http' in str(tag):
        tags.append(tag)
for tag in tags:
    items=str(tag).split(' ')
    # print(items[3])
    address=items[2][5:].replace('\"', '')
    print("address is :%s"%address)
    tagName=items[3].split('>')[1].split('<')[0]
    print(tagName)

