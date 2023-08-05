import json
import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zlsrc.util.etl import est_tbs, est_meta, est_html, est_gg, est_meta_large


def f1(driver,num):
    locator = (By.XPATH, '//table[@id="data_tab"]//tr[2]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum = driver.find_element_by_xpath('//a[@class="one"]').text.strip()

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//table[@id="data_tab"]//tr[2]//a').get_attribute('href')[-30:-5]

        driver.execute_script("pagination({});return false;".format(num))

        locator = (By.XPATH, '//table[@id="data_tab"]//tr[2]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('table', id='data_tab')
    trs = div.find_all('tr')[1:]
    if 'jsgcBgtz' in url:
        data=parse_2(trs)

    elif ('jsgcZbjggs' in url) or ('zbjggs' in url):
        data=parse_4(trs)

    elif ('jsgcZbyc' in url) or ('zfcgYcgg' in url):
        data=parse_3(trs)
    else:
        data=parse_1(trs)


    df=pd.DataFrame(data=data)

    return df
def parse_1(trs):
    data=[]
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[2].a['href']
        name = tds[2].a['title']
        index_num = tds[1].get_text()
        ggstart_time = tds[3].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.yn.gov.cn' + href

        diqu=tds[2].a.get_text().strip()
        diqu=re.findall('^\[(.+?)\]',diqu)[0]

        info = {'index_num': index_num,'diqu':diqu}
        info = json.dumps(info, ensure_ascii=False)
        tmp = [ name, href, ggstart_time,info]
        data.append(tmp)
    return data

def parse_2(trs):
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        index_num = tds[1].get_text()
        title = tds[2].get_text()
        href = tds[3].a['href']
        name = tds[3].a['title']
        ggstart_time = tds[4].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.yn.gov.cn' + href

        diqu = tds[3].a.get_text().strip()
        diqu = re.findall('^\[(.+?)\]', diqu)[0]
        info = {'index_num': index_num,'title':title,'diqu':diqu}

        info = json.dumps(info, ensure_ascii=False)
        tmp = [ name, href, ggstart_time,info]
        data.append(tmp)
    return data

def parse_3(trs):
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        index_num = tds[1].get_text()

        href = tds[2].a['href']
        name = tds[2].a['title']
        yctype = tds[3].get_text()
        ggstart_time = tds[4].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.yn.gov.cn' + href
        diqu = tds[2].a.get_text().strip()
        diqu = re.findall('^\[(.+?)\]', diqu)[0]
        info = {'index_num': index_num,'yctype':yctype,'diqu':diqu}
        info = json.dumps(info, ensure_ascii=False)
        tmp = [ name, href, ggstart_time,info]
        data.append(tmp)
    return data

def parse_4(trs):
    data = []
    for tr in trs:
        tds = tr.find_all('td')

        href = tds[1].a['href']
        name = tds[1].a['title']

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.yn.gov.cn' + href

        diqu = tds[1].a.get_text().strip()
        diqu = re.findall('^\[(.+?)\]', diqu)[0]

        info=json.dumps({'diqu':diqu},ensure_ascii=False)
        tmp = [name,href,ggstart_time,info]
        data.append(tmp)

    return data


def f2(driver):
    locator = (By.XPATH, '//table[@id="data_tab"]//tr[2]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//div[@class="mmggxlh"]/a[last()-1]').text
    total = int(page)
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="page_contect bai_bg"]')

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

    div = soup.find('div',class_="page_contect bai_bg")

    return div

data=[
    #
    ["gcjs_zhaobiao_gg","http://ggzy.yn.gov.cn/jyxx/jsgcZbgg",[ "name", "href", "ggstart_time", "info"],f1,f2],

    ["gcjs_gqita_da_bian_gg","http://ggzy.yn.gov.cn/jyxx/jsgcBgtz",[ "name", "href", "ggstart_time", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://ggzy.yn.gov.cn/jyxx/jsgcpbjggs",[ "name", "href", "ggstart_time", "info"],f1,f2],

    ["gcjs_zhongbiao_gg","http://ggzy.yn.gov.cn/jyxx/jsgcZbjggs",["name", "href", "ggstart_time", "info"],f1,f2],

    ["gcjs_liubiao_gg","http://ggzy.yn.gov.cn/jyxx/jsgcZbyc",["name", "href", "ggstart_time", "info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://ggzy.yn.gov.cn/jyxx/zfcg/cggg",[ "name", "href", "ggstart_time", "info"],f1,f2],

    ["zfcg_gqita_da_bian_gg","http://ggzy.yn.gov.cn/jyxx/zfcg/gzsx",[ "name", "href", "ggstart_time", "info"],f1,f2],

    ["zfcg_zhongbiaohx_gg","http://ggzy.yn.gov.cn/jyxx/zfcg/zbjggs",["name", "href", "ggstart_time", "info"],f1,f2],

    ["zfcg_liubiao_gg","http://ggzy.yn.gov.cn/jyxx/zfcg/zfcgYcgg",["name", "href", "ggstart_time", "info"],f1,f2],

]

def work(conp,**args):
    est_meta_large(conp,data=data,diqu="云南省",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","yunnan_new","yunnan2"]

    work(conp=conp,total=2,num=1)