import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import sys 
import time

import json
from zlsrc.util.etl import est_meta,est_html


def f1(driver,num):
    locator=(By.XPATH,"//div[@class='ewb-r-bd']/ul/li//a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    #url=driver.current_url
    cnum=int(re.findall("([0-9]{1,}).html",driver.current_url)[0])
    if num!=cnum:
        url=re.sub("[0-9]{1,}(?=\.html)",str(num),driver.current_url)
        val=driver.find_element_by_xpath("//div[@class='ewb-r-bd']/ul/li[1]//a").text.strip() 
        driver.get(url)

        locator=(By.XPATH,"//div[@class='ewb-r-bd']/ul/li[1]//a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    page=driver.page_source

    soup=BeautifulSoup(page,"html.parser")

    div=soup.find("div",class_="ewb-r-bd")
    ul=div.find("ul")
    lis=ul.find_all("li",class_="ewb-com-item clearfix jiezhi")

    data=[]

    for li in lis:
        a=li.find("a")
        spans=li.find_all("span",recursive=False)
        name=a.text.strip()
        name=re.sub("\[.*\]","",name)
        tmp=[name,spans[0].text.strip(),"http://www.zzsggzy.com"+a["href"]]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=json.dumps({"ggend_time":spans[1].text.strip()},ensure_ascii=False)
    return df 


def f2(driver):
    
    try:
        locator=(By.XPATH,"//li[contains(@class,'ewb-page-num')]//a[contains(string(),'末页')]")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        href=driver.find_element_by_xpath("//li[contains(@class,'ewb-page-num')]//a[contains(string(),'末页')]").get_attribute("href")

        total=re.findall("([0-9]{1,}).html",href)[0]
        total=int(total)
    except:
        total=1
    driver.quit()
    return total



def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"ewb-list-bd")

    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))

    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source

    soup=BeautifulSoup(page,'html.parser')

    div=soup.find('div',class_='ewb-list-bd')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div

data=[

        ["gcjs_zhaobiao_gg","http://www.zzsggzy.com/jsgc/004001/1.html",["name","ggstart_time","href","info"],f1,f2],

        ["gcjs_biangeng_gg","http://www.zzsggzy.com/jsgc/004002/1.html",["name","ggstart_time","href","info"],f1,f2],


        ["gcjs_zhongbiaohx_gg","http://www.zzsggzy.com/jsgc/004004/1.html",["name","ggstart_time","href","info"],f1,f2],

        ["gcjs_zhongbiao_gg","http://www.zzsggzy.com/jsgc/004003/1.html",["name","ggstart_time","href","info"],f1,f2],

        ["zfcg_zhaobiao_gg","http://www.zzsggzy.com/zfcg/005001/1.html",["name","ggstart_time","href","info"],f1,f2],

        ["zfcg_biangeng_gg","http://www.zzsggzy.com/zfcg/005002/1.html",["name","ggstart_time","href","info"],f1,f2],


        ["zfcg_zhongbiaohx_gg","http://www.zzsggzy.com/zfcg/005003/1.html",["name","ggstart_time","href","info"],f1,f2],


    ]

def work(conp,**args):
    est_meta(conp,data=data,diqu="河南省郑州市",**args)
    est_html(conp,f=f3,**args)


if __name__=="__main__":
    work(conp=["postgres","since2015","127.0.0.1","henan","zhengzhou"])