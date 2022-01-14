from selenium import webdriver
import time
from bs4 import BeautifulSoup
import threading
import requests


def find_artical(keyword):
    anslist=[]
    def threadworker(n):
        source=requests.get('https://ifoodie.tw'+centerlist[n]['href'][:30])
        soupprime=BeautifulSoup(source.text, 'html.parser')
        dirtyjson=soupprime.find_all('script',{'type':"text/javascript"})[-1]
        dirtyjson=dirtyjson.getText()
        urlstart=dirtyjson.find('"url"')
        urlend=dirtyjson.find('"is_paid"')
        anslist.append([arnamelist[n].getText(),dirtyjson[urlstart+8:urlend-3]])
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get('https://ifoodie.tw/search?q='+keyword)
    time.sleep(1)
    soup=BeautifulSoup(chrome.page_source, 'html.parser')
    centerlist=soup.find_all('a',{'class':'readmore'})
    arnamelist=soup.find_all('div',{'class':'title media-heading'})
    chrome.quit()
    threadlist=[]
    for i in range(len(centerlist)):
        threadlist.append(threading.Thread(target=threadworker, args=(i,)))
    for i in threadlist:
        i.start()
    for i in threadlist:
        i.join()
    return anslist

# print(find_artical('包子'))





