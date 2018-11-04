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

base_url='https://tieba.baidu.com'
#page_urls 贴吧每一页的地址
page_urls=['https://tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&ie=utf-8&pn={pn}'.format(pn=pn) for pn in range(200, 50850) if pn % 50 is 0]
#post_urls 每一个帖子的地址
post_urls=[]
save_path=r"F:\Study-Work\CrawThing\Heisiba"
img_num=2795

ssl._create_default_https_context=ssl._create_unverified_context()

def save_img(img_url, save_path):
    global img_num
    try:
        time.sleep(0.10)
        img = requests.get(img_url, headers=headers, timeout=10)
        img_name = "F:\Study-Work\CrawThing\Heisiba\pic_cnt_%d.jpg"%img_num
        with open(img_name, 'ab') as f:
            f.write(img.content)
            print(img_name)
        img_num+=1
    except Exception as e:
        print(e)
    pass

def get_img_urls(url):
    urls=[]
    html=requests.get(url, headers=headers).text
    imgtag=BeautifulSoup(html, 'lxml').find_all('img', class_='BDE_Image')
    results=re.findall(r"(?<=src=)\S+", str(imgtag))
    if results :
        urls= [url.replace('"', "") for url in results]
    return urls

def get_onePage_image(url):
    img_urls=get_img_urls(url)
    for img_url in img_urls:
        save_img(img_url, save_path)

def get_pageNum_of_post(post_url):
    html = requests.get(post_url, headers=headers).text
    tag = BeautifulSoup(html, 'lxml').find('div', class_='pb_footer').find_all('span', class_='red')[1]
    print("tag", tag)
    pageNum = int(re.findall(r"\d+", str(tag))[0])
    print('pageNum is :', pageNum)
    return pageNum

def get_post_image(post_url):
    pagenum=get_pageNum_of_post(post_url)
    for num in range(1, pagenum+1):
        url=post_url+'?pn={pn}'.format(pn=num)
        print("get_onePage_image")
        get_onePage_image(url)

def get_urlof_pages():
    for page_url in page_urls:
        post_urls=[]
        print("page_url is:", page_url)
        page_html=requests.get(page_url, headers=headers).text
        atag=BeautifulSoup(page_html, 'lxml').find_all('a', class_='j_th_tit ')
        result=re.findall(r"(?<=href=)\S+", str(atag))
        post_url_index = [url.replace('"', "") for url in result]
        post_url=map(lambda x:base_url+x , post_url_index)
        post_urls.extend(post_url)
        print("post_urls is:", post_urls)
        for url in post_urls:
            print("get_post_image:", url)
            get_post_image(url)

if __name__ == "__main__":
    get_urlof_pages()
    pass
