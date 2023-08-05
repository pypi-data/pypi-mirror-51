import json
import math
import random
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zlsrc.util.etl import  est_html,est_meta_large




def f1(driver,num):
    locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = int(driver.find_element_by_xpath('//li[@class="active"]/a').text)
    if num != cnum:
        val = driver.find_element_by_xpath('//ul[@class="wb-data-item"]/li[1]//a').get_attribute('href')[-40:-5]

        search_button = driver.find_element_by_xpath('//input[@data-page-btn="jump"]')
        driver.execute_script("arguments[0].value='%s';" % num, search_button)
        ele = driver.find_element_by_xpath('//button[@data-page-btn="jump"]')
        driver.execute_script("arguments[0].click()", ele)

        locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lis = soup.find_all('li', class_='wb-data-list')
    for li in lis:
        href = li.find('a')['href']
        name = li.find('a')['title']
        diqu = li.find('span', class_='ewb-c01').get_text().strip('【').strip('】')
        ggstart_time = li.find('span', class_='wb-data-date').get_text()
        info = {'diqu': diqu}
        info = json.dumps(info, ensure_ascii=False)
        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.hebei.gov.cn' + href
        tmp = [name, ggstart_time, href, info]

        data.append(tmp)
    df = pd.DataFrame(data=data)

    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = \
        re.findall('<div class="m-pagination-info" style="display: none;">.+?of(.+?)entires.*?</div>',
                   driver.page_source)[0]
    total = math.ceil(int(total.strip()) / 10)

    driver.quit()
    return total




def chang_type(f,markstr):

    def inner(*args):
        driver=args[0]
        try:
            locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]//a')
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]//a')
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))

        ctext=driver.find_element_by_xpath('//ul[@id="categorylist"]//a[@class="current"]').text.strip()

        if '全部' in ctext:
            marktotal = \
                re.findall('<div class="m-pagination-info" style="display: none;">.+?of(.+?)entires.*?</div>',
                           driver.page_source)[0]
            ele=driver.find_element_by_xpath('//a[@data-val="%s"]'%markstr)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click()", ele)
            WebDriverWait(driver,10).until(lambda driver:re.findall('<div class="m-pagination-info" style="display: none;">.+?of(.+?)entires.*?</div>',
                           driver.page_source)[0] != marktotal)

        return f(*args)

    return inner


def f3(driver, url):
    driver.get(url)
    try:
        locator = (By.XPATH, '//div[@id="content"][string-length()>100] | //div[@id="hideDeil"][@style=""][string-length()>100]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        flag = 1
    except:
        driver.find_element_by_xpath('//div[@id="hideDeil"][@style="display:none"][string-length()>100]')
        flag = 2

    before = len(driver.page_source)
    time.sleep(0.5)
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

    if flag == 2:
        div = soup.find('div', class_="ewb-main")
        div.find('div', attrs={"id": "hideDeil", "style": "display:none"})['style']=""
    elif flag == 1:
        div = soup.find('div', class_="ewb-main")
    else:raise ValueError
    if div == None:
        raise ValueError
    return div




data=[
        #
    ["gcjs_zhaobiao_gg", "http://ggzy.hebei.gov.cn/jyggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'jsgc'), chang_type(f2,'jsgc'),],
    ["zfcg_zhaobiao_gg", "http://ggzy.hebei.gov.cn/jyggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'zfcg'), chang_type(f2,'zfcg'),],
    ["jqita_zhaobiao_gg", "http://ggzy.hebei.gov.cn/jyggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'qt'), chang_type(f2,'qt'),],

    ["gcjs_zhongbiaohx_gg", "http://ggzy.hebei.gov.cn//cjggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'jsgccj'), chang_type(f2,'jsgccj'),],
    ["zfcg_zhongbiaohx_gg", "http://ggzy.hebei.gov.cn//cjggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'zfcgcj'), chang_type(f2,'zfcgcj'),],
    ["jqita_zhongbiaohx_gg", "http://ggzy.hebei.gov.cn//cjggiframe.html?GG_CITY=&GG_GOUNTY=&GG_CATETOP=",['name', 'ggstart_time', 'href', 'info'], chang_type(f1,'qtcj'), chang_type(f2,'qtcj'),],

]


def work(conp,**args):
    est_meta_large(conp,data=data,diqu="河北省河北",interval_page=800, **args)
    est_html(conp,f=f3,**args)



# 更新日期：2019/7/8
if __name__=='__main__':
    #
    conp=["postgres","since2015","192.168.3.171","hebei","hebei_new"]

    work(conp=conp,pageloadtime=60,headless=False,total=5,num=1)

    # for d in data:
    #     driver=webdriver.Chrome()
    #     url=d[1]
    #     print(url)
    #     driver.get(url)
    #     df = f2(driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #
    #     df=f1(driver, 2)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)
    # driver = webdriver.Chrome()
    # df  = f3(driver, 'http://ggzy.hebei.gov.cn/fwdt/003005/003005001/003005001001/20180118/ffb6da6b-918b-4c84-a180-af78306c2ffa.html')
    # print(df)
