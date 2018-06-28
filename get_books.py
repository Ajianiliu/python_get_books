#-*- coding: UTF-8 -*- 
import requests
import codecs
import sys
import re

from bs4 import BeautifulSoup
from notebook.services import contents
from numba.tests.test_builtins import abs_usecase


def getContent(content_url):
    #print(content_url)
    res = requests.get(content_url,timeout=10)
    #print(type(res))
    #print("res: ",res)
    res.encoding = 'gbk'
    #print("encoding: ", res.encoding)
    #print("text: ", res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    titles = soup.select('.jieqi_title')
    if len(titles) == 0:
        print("!!!!!!!!!!!!len(titles) == 0")
        return getContent(content_url)
    else:
        title = titles[0].text.lstrip(u'章 节目录 ')
    #[0].text.lstrip(u'章 节目录 ')
    #print("type:", type(title),title)
    #print title.encode('utf-8')
    content = soup.select('#content')[0].text.lstrip('style5();').rstrip('style6();')
    #print(content)
    both = title + content
    return both

def getCatalog(catalog_url):
    #print(catalog_url)
    res = requests.get(catalog_url, timeout=10)
    #print(type(res))
    #print("res: ",res)
    res.encoding = 'gbk'
    #print("encoding: ", res.encoding)
    #print("text: ", res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    
    catalogs = soup.find_all("a", href=re.compile(catalog_url))#[0].text.lstrip(u'章 节目录 ')
    #catalogs = soup.select('#content')
    '''
    catalog_len = len(catalogs)
    for num in range(0, catalog_len):
        catalog_ref = catalogs[num].get('href')
        #print(type(catalog_num))
        print catalog_ref
        #print(catalog[num].href)
    '''    
    #print("type:", type(catalog),catalog)
    #print title[0].encode('utf-8')
    #content = soup.select('#content')[0].text.lstrip('style5();').rstrip('style6();')
    #print(content)
    #both = title + content
    return catalogs
    
def get_one_book(url):
    i = 0
    f = codecs.open("dldl.txt", 'w+', 'utf-8')
    f_debug = codecs.open("debug.txt", 'w+', 'utf-8')
    
    catalog = getCatalog(url)
    
    catalog_count = len(catalog)
    if catalog_count == 0:
        print("!!!!!no catalog, END get book from", url)
        return
    for num in range(0, catalog_count):
        catalog_ref = catalog[num].get('href')
        contents = getContent(catalog_ref)
        print >> f, contents
        i=i+1
        url_debug = catalog_ref+"__"+str(i)
        print(url_debug)
        print >> f_debug,url_debug

    f.close()
    print('ok!!!')
    return

def get_books():
    url='http://www.quanshuwang.com/book/44/44683'
    print 'start get_books from', url
    get_one_book(url)
    return
#MAIN--
get_books()