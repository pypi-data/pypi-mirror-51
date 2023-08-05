import time
from collections import OrderedDict
from os.path import join, dirname
from pprint import pprint

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zlsrc.util.etl import est_meta, est_html, add_info, est_meta_large


def f1(driver,num):
    locator=(By.XPATH,'//div[@class="pagingList"]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    cnum = driver.find_element_by_xpath('//a[@class="curpage"]').text
    url=driver.current_url
    main_url=url.rsplit('/',maxsplit=1)[0]
    if int(cnum) != num:
        if num==1:
            url=main_url+'/index.htm'
        else:
            url=main_url+'/index_'+str(num-1)+'.htm'
        val=driver.find_element_by_xpath('//div[@class="pagingList"]/ul/li[1]/a').get_attribute('href')[-20:-2]

        driver.get(url)
        locator=(By.XPATH,'//div[@class="pagingList"]/ul/li[1]/a[not(contains(@href,"%s"))]'%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('div', class_='pagingList')
    data = []
    url = driver.current_url
    main_url = url.rsplit('/',maxsplit=1)[0]
    urs = trs.find_all('li')
    for tr in urs:
        href = tr.a['href'].strip('.')
        name = tr.a.get_text().strip()
        ggstart_time = tr.span.get_text()

        if re.findall('http', href):
            href = href
        else:
            href = main_url + href
        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):

    locator = (By.XPATH, "//div[@class='pagingList']/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.find_element_by_xpath('//*[@id="div_page"]/a[last()]').get_attribute('href')
    total_ = re.findall(r'index_(\d+).htm', page)[0]

    driver.quit()
    return int(total_)


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="text clear"][string-length()>10]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div',class_='text clear')
    return div





def get_data():
    data = []

    #gcjs
    ggtype1 = OrderedDict([("zhaobiao","zbgg"),("gqita_da_bian", "dyby"), ("zhongbiaohx", "zbgs")])
    #zfcg
    ggtype2 = OrderedDict([("zhaobiao","zbgg"),("gqita_da_bian", "dyby"), ("zhongbiao", "zbgs")])

    ##zfcg_gcjs
    adtype1 = OrderedDict([('市本级','jas,01'),("吉安县", "jax,02"), ("新干县", "xgx,03"),("永丰县","yfx,04"),("陕江县","xjx,05"),
                           ('吉水县', 'jsx,06'), ("泰和县", "thx,07"), ("万安县", "wax,08"), ("遂川县", "scx,09"),('安福县',"afx,10"),
                           ('永新县',"yxx,11"),("井冈山市","jgss,12")])

    #gcjs
    for w1 in ggtype1.keys():
        for w2 in adtype1.keys():
            href = "http://ggzy.jian.gov.cn/jyxx/jsgc/{jy}/{dq}/index.htm".format(dq=adtype1[w2].split(',')[0],jy=ggtype1[w1])
            tmp = ["gcjs_%s_diqu%s_gg" % (w1, adtype1[w2].split(',')[1]), href, ["name","ggstart_time","href",'info'],
                   add_info(f1, {"diqu": w2}), f2]
            data.append(tmp)

    ##zfcg
    for w1 in ggtype2.keys():
        for w2 in adtype1.keys():
            href = "http://ggzy.jian.gov.cn/jyxx/zfcg/{jy}/{dq}/index.htm".format(dq=adtype1[w2].split(',')[0],jy=ggtype2[w1])
            tmp = ["zfcg_%s_diqu%s_gg" % (w1, adtype1[w2].split(',')[1]), href, ["name","ggstart_time","href",'info'],
                   add_info(f1, {"diqu": w2}), f2]
            data.append(tmp)

    data1 = data.copy()


    return data1


data=get_data()
# pprint(data)



def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省吉安市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","jian1"]

    work(conp=conp,headless=False,num=1,total=10,ipNum=0)
    # work(conp=conp,headless=False,num=1,ipNum=0)