import pandas as pd  
import re 
from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import sys 
import time
from zlsrc.util.etl import  est_meta, est_html, add_info



def f1(driver,num):
    locator=(By.XPATH,"//div[@class='byTradingDetailMain']//dl[1]//a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//ul[@class='pagination pagination-outline']/li[@class='paginate_button active']/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum=int(driver.find_element_by_xpath("//li[@class='paginate_button active']/a").text)
    if cnum!=num:
        page_count = len(driver.page_source)
        val=driver.find_element_by_xpath('//div[@class="byTradingDetailMain"]//dl[1]//a').get_attribute('href')
        val = re.findall(r'/f/(.+)$', val)[0]

        driver.execute_script("page(%d,20,'');"%num)
        locator = (
            By.XPATH, "//div[@class='byTradingDetailMain']//dl[1]//a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        WebDriverWait(driver, 10).until(lambda driver: len(driver.page_source) != page_count)
    page=driver.page_source
    soup=BeautifulSoup(page,'html.parser')
    div=soup.find("div",class_="byTradingDetailMain")
    dls=div.find_all("dl")
    data=[]
    for dl in dls:
        name=dl.find('a').get_text().strip().replace('\t','').replace('\n','').replace(' ','')
        href=dl.find('a')['href']
        ggstart_time=dl.find('span',class_='byTradingDetailTime').get_text()
        if 'http' in href:
            href=href
        else:
            href='http://www.jygzyjy.gov.cn'+href
        tmp=[name,ggstart_time,href]

        data.append(tmp)



    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 


def f2(driver):
    locator = (By.XPATH, "//div[@class='byTradingDetailMain']//dl[1]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator=(By.XPATH,"//ul[@class='pagination pagination-outline']/li[@class='paginate_button active']/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    try:
        total=int(driver.find_element_by_xpath('//li[@class="paginate_button "][last()]/a').text)
    except:
        total=1

    driver.quit()
    return total

def f3(driver,url):


    driver.get(url)

    locator=(By.XPATH,'//div[@class="jxTradingMainLayer clear"][string-length()>100]')

    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

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
    div=soup.find('div',class_='jxTradingMainLayer clear')
    if not div:
        raise ValueError

    return div


data=[

["gcjs_zhaobiao_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=1",["name","ggstart_time","href","info"],f1,f2],
["gcjs_zgysjg_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=1&index=2",["name","ggstart_time","href","info"],f1,f2],
["gcjs_zhongbiaohx_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=1&index=3",["name","ggstart_time","href","info"],f1,f2],
["gcjs_zhongbiao_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=1&index=4",["name","ggstart_time","href","info"],f1,f2],

["zfcg_zhaobiao_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=2&index=1",["name","ggstart_time","href","info"],f1,f2],
["zfcg_zhongbiaohx_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=2&index=3",["name","ggstart_time","href","info"],f1,f2],
["zfcg_zhongbiao_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=2&index=4",["name","ggstart_time","href","info"],f1,f2],

["zfcg_zhaobiao_xieyi_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=5",["name","ggstart_time","href","info"],add_info(f1,{'zbfs':'协议供货'}),f2],
["gcjs_zhaobiao_xiane_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=6",["name","ggstart_time","href","info"],add_info(f1,{'zbfs':'限额以下'}),f2],
["zfcg_zhaobiao_xiane_gg","http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=7",["name","ggstart_time","href","info"],add_info(f1,{'zbfs':'限额以下'}),f2],

    ]



##f3 是pdf

def work(conp,**args):
    est_meta(conp,data=data,diqu="甘肃省嘉峪关市",**args)
    est_html(conp,f=f3,**args)


if __name__=="__main__":
    work(conp=["postgres","since2015",'192.168.3.171',"gansu","jiayuguan"])
    # driver=webdriver.Chrome()
    # f3(driver,'http://www.jygzyjy.gov.cn/f/newtrade/tenderprojects/3632/flowpage?pageIndex=1&annogoodsId=2619')