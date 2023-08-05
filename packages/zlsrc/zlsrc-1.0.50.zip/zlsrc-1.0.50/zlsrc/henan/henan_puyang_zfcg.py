import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zlsrc.util.etl import est_meta, est_html, add_info




def f1(driver, num):
    locator = (By.XPATH, '//div[@class="List2"]//li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    cnum = re.findall('pageNo=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="List2"]//li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        url_ = main_url + '=%d' % num

        driver.get(url_)

        locator = (By.XPATH, '//div[@class="List2"]//li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='List2')
    lis = div.find_all('li')
    for li in lis:
        name = li.a.get_text()
        href = li.a['href']
        if 'http' in href:
            href=href
        else:
            href = "http://puyang.hngp.gov.cn" + href
        ggstart_time = li.span.get_text()

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//div[@class="List2"]//li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    try:
        driver.find_element_by_xpath('//div[@class="List2"]/ul[count(li)=20]')
    except:
        total = 1
        driver.quit()
        return total

    try:
        total = driver.find_element_by_xpath('//li[@class="lastPage"]/a').get_attribute('href')
        total = int(re.findall('pageNo=(\d+)', total)[0])
    except:
        url = re.sub('pageNo=\d+', 'pageNo=2', url)
        driver.get(url)
        locator = (By.XPATH, '//div[@class="List2"]/ul')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        c_text = driver.find_element_by_xpath('//div[@class="List2"]/ul').get_attribute('innerHTML').strip()

        if not c_text:
            total = 1
        else:
            total = driver.find_element_by_xpath('//li[@class="pageInfo"]').text
            total = int(re.findall('共(.+?)页', total)[0].strip())

    if total > 200:
        total = 200

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="content"]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    locator = (By.XPATH, '//div[@id="content"][string-length()>2] | //div[@id="content"][count(*)>=1]')
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
    div = soup.find('div', class_="BorderEEE BorderRedTop")
    div2 = soup.find('div', class_="List1 Top5")
    if div2:
        div = str(div) + str(div2)
        div = BeautifulSoup(div, 'html.parser')
    return div


data = [

     ["zfcg_zhaobiao_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=0101&bz=1&pageSize=20&pageNo=2",["name","ggstart_time", "href", 'info'], f1, f2],
    ##包含中标,流标
    ["zfcg_zhongbiao_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=0102&bz=1&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ##包含变更,流标
    ["zfcg_biangeng_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=0103&bz=1&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_dyly_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1301&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_gqita_jinkou_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1302&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], add_info(f1,{"tag":"进口商品"}), f2],
    ["zfcg_gqita_zhibiao_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1303&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], add_info(f1,{"tag":"技术指标"}), f2],

    ["zfcg_gqita_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1304&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_yanshou_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1402&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhaobiao_jingjia_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1201&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], add_info(f1,{"zbfs":"网上竞价"}), f2],

    ["zfcg_gqita_xieyi_gg", "http://puyang.hngp.gov.cn/puyang/ggcx?appCode=H70&channelCode=1009&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], add_info(f1,{"tag":"协议供货"}), f2],


]


def work(conp, **args):
    est_meta(conp, data=data, diqu="河南省濮阳市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "lch", "henan_puyang"]

    work(conp=conp)