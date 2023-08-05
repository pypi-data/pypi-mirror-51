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
    locator=(By.XPATH,"//ul[@class='wb-data-item']")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    #url=driver.current_url
    cnum=int(re.findall("\/([0-9]{1,}).html",driver.current_url)[0])
    if num!=cnum:
       
        val=driver.find_element_by_xpath("//ul[@class='wb-data-item']//li[1]//a").text.strip() 
        input1=driver.find_element_by_class_name("ewb-page-input")
        input1.clear()
        input1.send_keys(num)
        driver.execute_script("skip();")

        locator=(By.XPATH,"//ul[@class='wb-data-item']//li[1]//a[not(contains(string(),'%s'))]"%val)
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
        name=re.sub("\[.*\]","",name)
        tmp=[name,ggstart_time,"http://www.xzggzy.cn"+a["href"]]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 


def f2(driver):
    
    try:
        locator=(By.CLASS_NAME,"ewb-page-num")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        href=driver.find_element_by_class_name("ewb-page-num").text

        total=re.findall("\/([0-9]{1,})",href)[0]
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
    ["gcjs_zhaobiao_gg","http://www.xzggzy.cn/jyxx/005001/005001001/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_biangeng_gg","http://www.xzggzy.cn/jyxx/005001/005001002/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://www.xzggzy.cn/jyxx/005001/005001003/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_kongzhijia_gg","http://www.xzggzy.cn/jyxx/005001/005001004/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_yucai_gg","http://www.xzggzy.cn/jyxx/005002/005002001/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.xzggzy.cn/jyxx/005002/005002002/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_biangeng_gg","http://www.xzggzy.cn/jyxx/005002/005002003/1.html",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhongbiaohx_gg","http://www.xzggzy.cn/jyxx/005002/005002004/1.html",["name","ggstart_time","href","info"],f1,f2],


]






def work(conp,**args):
    est_meta(conp,data=data,diqu="河南省新郑市",**args)
    est_html(conp,f=f3,**args)


if __name__=="__main__":
    work(conp=["postgres","since2015","127.0.0.1","henan","xinzheng"])
    #work(conp=["postgres","since2015","127.0.0.1","henan","xinzheng"],num=1,total=2,html_total=10)