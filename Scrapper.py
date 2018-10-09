import os   
import time
from urllib.request import  urlopen  
from urllib  import request  
from bs4 import BeautifulSoup  
import pandas as pd
from selenium import webdriver
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}

##get pages
req=request.Request("https://www.xiami.com/artist/album-cZYi3abc5?spm=a1z1s.6659509.6856549.3.9HSpLu",headers=headers)
html=urlopen(req)
bsObj=BeautifulSoup(html.read(),"html.parser")
tags = bsObj.find_all('a','p_num')
half_urls_of_pages=[]
for tag in tags:
    half_urls_of_pages.append(tag.get('href'))
urls_of_pages=["https://www.xiami.com"+s for s in half_urls_of_pages[1::]]+["https://www.xiami.com/artist/album-cZYi3abc5?spm=a1z1s.6659509.6856549.3.9HSpLu"]

##get urls of albums on a certain page
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
def get_album_urls(urls):
    for url in urls:
        req=request.Request(url,headers=headers)
        html=urlopen(req)
        bsObj=BeautifulSoup(html.read(),"html.parser")
        tags = bsObj.find_all("p","name")
        urls_of_albums=[]
        for tag in tags:
            tags_of_a=tag.find_all('a')
            for tag_of_a in tags_of_a:
                urls_of_albums.append(tag_of_a.get('href'))
        return urls_of_albums
half_urls_of_albums=get_album_urls(urls_of_pages)

##get comment of an album in a page
urls_of_albums=["https://www.xiami.com"+s for s in half_urls_of_albums]
def get_comment(urls):
    for url in urls:
        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get(url)
        ##req=request.Request(url,headers=headers)
        ##html=urlopen(req)
        time.sleep(2)
        bsObj=BeautifulSoup(driver.page_source,"html.parser")
        bsObj=BeautifulSoup(html.read(),"html.parser")
        bs = bsObj.findAll(attrs={"class":"brief"})
        comment_in_a_page = []
        for bs1 in bs:
            comment_in_a_page.append(bs1.get_text().replace('\n','').replace('\t','').replace(' ',''))
        driver.close()
    return comment_in_a_page
