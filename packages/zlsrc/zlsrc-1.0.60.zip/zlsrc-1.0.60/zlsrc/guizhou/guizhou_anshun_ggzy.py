
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
    locator = (By.XPATH, '//li[@class="ewb-com-item"][1]//a')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located(locator))

    url=driver.current_url

    if "subpagejy.html" in url:
        cnum=1
    else:
        cnum = int(re.findall(r'/(\d+).html',url)[0])

    if cnum != num:
        page_count = len(driver.page_source)
        val=driver.find_element_by_xpath('//li[@class="ewb-com-item"][1]//a').get_attribute('href')[-30:-5]
        if num==1:
            url = re.sub("\d+.html", "subpagejy.html", url)
        else:
            url=re.sub("\/[subpagejy\d]*.html","/%d.html"%num,url)

        driver.get(url)
        locator=(By.XPATH,'//li[@class="ewb-com-item"][1]//a[not(contains(@href,"%s"))]'%val)
        WebDriverWait(driver,40).until(EC.presence_of_element_located(locator))

        WebDriverWait(driver, 40).until(lambda driver: len(driver.page_source) != page_count)

    page=driver.page_source
    soup=BeautifulSoup(page,"html.parser")
    div=soup.find('div',class_="ewb-right-bd").find('ul').find_all("li")

    data=[]
    for li in div:
        a=li.find("a")
        name=a.get_text()
        href=a['href']
        ggstart_time=li.find("span",class_="r").get_text()

        diqu=re.findall('^\[(.+?)\]',name)
        gctype=re.findall('\]\[(.+?)\]',name)
        diqu=diqu[0] if diqu else None
        gctype=gctype[0] if gctype else None

        info =json.dumps({'diqu':diqu,'gctype':gctype},ensure_ascii=False)

        tmp=[name,"http://ggzy.anshun.gov.cn"+href,ggstart_time,info]

        # print(tmp)
        data.append(tmp)

    df=pd.DataFrame(data=data)

    return df


def f2(driver):
    locator=(By.XPATH,'//li[@class="ewb-com-item"][1]//a')
    WebDriverWait(driver,40).until(EC.presence_of_element_located(locator))

    atext=driver.find_element_by_xpath("//li[@id='index']").text.strip()

    total=int(atext.split("/")[1])

    driver.quit()

    return total



def f3(driver,url):

    driver.get(url)

    locator=(By.XPATH,'//div[@class="ewb-list-bd"][string-length()>50]')

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

    if div == None:
        raise ValueError('div is None')

    return div



data=[
["gcjs_zhaobiao_gg","http://ggzy.anshun.gov.cn/jyxx/003001/003001001/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["gcjs_zhongbiaohx_gg","http://ggzy.anshun.gov.cn/jyxx/003001/003001002/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["gcjs_liubiao_gg","http://ggzy.anshun.gov.cn/jyxx/003001/003001003/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["gcjs_gqita_da_bian_gg","http://ggzy.anshun.gov.cn/jyxx/003001/003001005/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],

["zfcg_zhaobiao_gg","http://ggzy.anshun.gov.cn/jyxx/003002/003002001/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["zfcg_zgysjg_gg","http://ggzy.anshun.gov.cn/jyxx/003002/003002004/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["zfcg_zhongbiaohx_gg","http://ggzy.anshun.gov.cn/jyxx/003002/003002002/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["zfcg_liubiao_gg","http://ggzy.anshun.gov.cn/jyxx/003002/003002003/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["zfcg_gqita_da_bian_gg","http://ggzy.anshun.gov.cn/jyxx/003002/003002005/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],

["qsy_zhaobiao_gg","http://ggzy.anshun.gov.cn/jyxx/003005/003005001/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],
["qsy_zhongbiaohx_gg","http://ggzy.anshun.gov.cn/jyxx/003005/003005002/subpagejy.html",["name","href","ggstart_time","info"],f1,f2],

]



def work(conp,**args):
    est_meta(conp,data=data,diqu="贵州省安顺市",**args)

    est_html(conp,f=f3,**args)

if __name__ == '__main__':

    work(conp=["postgres","since2015","192.168.3.171","guizhou","anshun"],num=1,ipNum=0,headless=False)