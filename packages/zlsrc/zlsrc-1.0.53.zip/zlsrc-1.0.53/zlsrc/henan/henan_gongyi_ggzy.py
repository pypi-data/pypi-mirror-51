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
from zlsrc.util.etl import est_meta,est_html,add_info



def f1(driver,num):
    locator=(By.XPATH,"//ul[@class='wb-data-item']/li//a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    #url=driver.current_url
    cnum=int(driver.find_element_by_xpath("//div[@id='divInfoReportPage']//span[@class='current pageIdx']").text.strip())
    if num!=cnum:
       
        val=driver.find_element_by_xpath("//ul[@class='wb-data-item']//li[1]//a").get_attribute('href')[-30:]
        input1=driver.find_element_by_class_name("pg_num_input")
        input1.clear()
        input1.send_keys(num)
        driver.find_element_by_class_name("pg_gobtn").click()

        locator=(By.XPATH,"//ul[@class='wb-data-item']//li[1]//a[not(contains(@href,'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    page=driver.page_source

    soup=BeautifulSoup(page,"html.parser")

    ul=soup.find("ul",class_='wb-data-item')

    lis=ul.find_all("li")

    data=[]

    for li in lis:
        a=li.find("a")
        ggstart_time=li.find("span").text.strip()
        name=a.text.strip()
        #name=re.sub("\[.*\]","",name)
        tmp=[name,ggstart_time,"http://www.gyggzyjy.gov.cn"+a["href"]]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 


def f2(driver):
    
    try:
        locator=(By.ID,"divInfoReportPage")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        total=driver.find_element_by_xpath("//div[@id='divInfoReportPage']//span[@class='pg_maxpagenum']").text.split("/")[1]


        total=int(total)
    except:
        total=1
    driver.quit()
    return total



def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"news-article")

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

    div=soup.find('div',class_='news-article')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div



data=[
    ["gcjs_zhaobiao_gg","http://www.gyggzyjy.gov.cn/gcjs/006001/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_biangeng_gg","http://www.gyggzyjy.gov.cn/gcjs/006002/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://www.gyggzyjy.gov.cn/gcjs/006003/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_liubiao_gg","http://www.gyggzyjy.gov.cn/gcjs/006005/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_yucai_gg","http://www.gyggzyjy.gov.cn/zfcg/007001/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.gyggzyjy.gov.cn/zfcg/007002/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_biangeng_gg","http://www.gyggzyjy.gov.cn/zfcg/007003/honest-list.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhongbiaohx_gg","http://www.gyggzyjy.gov.cn/zfcg/007004/honest-list.html",["name","ggstart_time","href","info"],f1,f2],


]






def work(conp,**args):
    est_meta(conp,data=data,diqu="河南省巩义市",**args)
    est_html(conp,f=f3,**args)


if __name__=="__main__":
    work(conp=["postgres","since2015","127.0.0.1","henan","gongyi"])