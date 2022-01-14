from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import cv2
import numpy as np
import os
def find_menu(keyword):
    uniKeyword = str(keyword.encode('unicode_escape'))
    uniKeyword = uniKeyword.replace("'", '')
    uniKeyword = uniKeyword.replace('\\', '')
    if os.path.isfile('./crawl/menu/'+uniKeyword+'.png'):
        print('Menu Had Been Found!')
        return('./crawl/menu/'+uniKeyword+'.png')
    print('Initiating...')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get('https://www.google.com.tw/maps')
    print('Crawling...')
    searchbar=chrome.find_element(By.XPATH,'//*[@id="searchboxinput"]')
    searchbar.send_keys(keyword)
    searchbotton=chrome.find_element(By.XPATH,'//*[@id="searchbox-searchbutton"]')
    searchbotton.click()
    time.sleep(3)
    print('25%')
    urlnow=chrome.current_url
    if 'search' in urlnow:
        try:
            firststore=chrome.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/a')
        except:
            firststore=chrome.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a')

        firststore.click()
    else:
        pass
    time.sleep(3)
    picbotton=chrome.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[1]/div[1]/button/img')
    picbotton.click()
    print('50%')
    time.sleep(2)
    soup=BeautifulSoup(chrome.page_source, 'html.parser')
    buttonlist=soup.find_all('div',{'class':"Gpq6kf gm2-button-alt"})
    buttonlisttext=[]
    for i in buttonlist:
        buttonlisttext.append(i.getText())
    # print(buttonlisttext)
    menubotindex=buttonlisttext.index('菜單')

    menubotton=chrome.find_element(By.XPATH,f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div/div/button[{menubotindex+1}]')
    menubotton.click()
    time.sleep(2)
    print('75%')
    souhebutton=chrome.find_element(By.XPATH,'//*[@id="pane"]/div/div[3]/button')
    souhebutton.click()
    time.sleep(3)
    chrome.save_screenshot("./crawl/screenshot.png")
    chrome.quit()

    before=cv2.imread('./crawl/screenshot.png')

    after=before.copy()

    B, G, R = cv2.split(after)
    height=len(B)
    wid=len(B[0])
    alpha = np.ones(B.shape, dtype=B.dtype) * 255
    # for i in range(980,1060):
        # for j in range(700,900):
        #     if  (i-1020)**2+(j-740)**2<1550 :
        #         B[i][j]+=50
        #         G[i][j]+=50
        #         R[i][j]+=50
        #         if B[i][j]>255:B[i][j]=200
        #         if G[i][j]>255:G[i][j]=200
        #         if R[i][j]>255:R[i][j]=200
        #     if  (i-1020)**2+(j-860)**2<1550:
        #         B[i][j]+=100
        #         G[i][j]+=100
        #         R[i][j]+=100
        #         if B[i][j]>255:B[i][j]=200
        #         if G[i][j]>255:G[i][j]=200
        #         if R[i][j]>255:R[i][j]=200
    for i in range(1000):
        if B[height//3,i]!=0 or G[height//3,i]!=0 or R[height//3,i]!=0:
            start=i
            break
    for i in range(1,1000):
        if B[height//2,wid-i]!=0 or G[height//2,wid-i]!=0 or R[height//2,wid-i]!=0:
            end=wid-i
            break
    alpha[:,:]=0
    alpha[:,start:end]=255
    saved = cv2.merge((B[:,start:end], G[:,start:end], R[:,start:end], alpha[:,start:end]))

    # cv2.imshow('image', saved)
    cv2.imwrite('./crawl/menu/'+uniKeyword+'.png', saved)
    print('100%\nMenu Has Been Found!')
    #cv2.destroyAllWindows()
    return('./crawl/menu/' +uniKeyword+'.png')
    # return('./crawl/screenshot.png')
# print(find_menu('三媽'))


'''
before=cv2.imread('screenshot.png')
after=before.copy()
b_channel, g_channel, r_channel = cv2.split(after)
print(type(b_channel))
alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
for i in range(1000):
    if b_channel[500,i]!=0:
        start=i
        break
for i in range(1000):
    if b_channel[500,1599-i]!=0:
        end=1599-i
        break
alpha_channel[:,:]=0
alpha_channel[:,start:end]=255
saved = cv2.merge((b_channel[:,start:end], g_channel[:,start:end], r_channel[:,start:end], alpha_channel[:,start:end]))

cv2.imwrite("noback.png", saved)
cv2.destroyAllWindows()
'''