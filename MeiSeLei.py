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

page_urls=['http://tieba.baidu.com/f/fdir?fd=%C7%E9%B8%D0&sd=%C3%C0%C9%AB&pn={pn}'.format(pn=pn) for pn in range(1, 14) ]
ssl._create_default_https_context=ssl._create_unverified_context()

def getAllTags():
    filterTags = []
    for page_url in page_urls:
        html=requests.get(page_url, headers=headers).text
        results=BeautifulSoup(html, 'lxml').find_all('td')
        for tag in results:
            if 'http' and 'kw=%' in str(tag):
                filterTags.append(tag)
    return filterTags

def parseTagNameAndAddress(tag):
    items=str(tag).split(' ')
    address=items[2][5:].replace('\"', '')
    tagName=items[3].split('>')[1].split('<')[0]
    return address, tagName

if __name__=='__main__':
    visible=notvisible=0
    dlTag=[]
    tags=getAllTags()
    for tag in tags:
        dtag={}
        dtag['address'], dtag['name']=parseTagNameAndAddress(tag)
        dlTag.append(dtag)

    for dtag in dlTag:
        html=requests.get(dtag['address'], headers=headers).text
        Title=str(BeautifulSoup(html, 'lxml').title).split('>')[1].split('<')[0].strip()
        if Title==u'百度贴吧':
            visible+=1
            dtag['visible']=u'不可访问'
            print(dtag['name'], "不可访问")
        else:
            notvisible+=1
            print(dtag['name'], "可以")
    print('visible %d'%visible)
    print('notvisible %d'%notvisible)
    pass
