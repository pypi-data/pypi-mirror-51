import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from zlsrc.util.etl import est_tbs, est_meta, est_html



def f1(driver, num):
    locator = (By.XPATH, '//ul[@class="list"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    cnum = driver.find_element_by_xpath('//span[@class="pagenav-cur"]').text

    if cnum != str(num):
        val = driver.find_element_by_xpath('//ul[@class="list"]/li[1]/a').get_attribute('href')[-15:]

        if num == 1:
            url = url.rsplit('/', maxsplit=1)[0] + '/index.html'
        else:
            url = re.sub('index_{0,1}\d*.html', 'index_%s.html' % (num - 1), url)

        driver.get(url)

        locator = (By.XPATH, '//ul[@class="list"]/li[1]/a[not(contains(@href,"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('ul', class_="list").find_all('li')
    for tr in trs:
        href = tr.a['href'].strip('.')
        name = tr.a['alt']
        ggstart_time = tr.span.get_text()
        if 'http' in href:
            href = href
        else:
            href = url.rsplit('/', maxsplit=1)[0] + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@class="list"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    while True:
        val = driver.find_element_by_xpath('//ul[@class="list"]/li[1]/a').get_attribute('href')[-15:]
        try:
            driver.find_element_by_link_text('下5页').click()
        except:
            driver.find_element_by_link_text('下一页').click()
        locator = (By.XPATH, '//ul[@class="list"]/li[1]/a[not(contains(@href,"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        cnum = int(driver.find_element_by_xpath('//span[@class="pagenav-cur"]').text)
        max_num = driver.find_element_by_xpath('//div[@class="paging"]/a[last()]').get_attribute('href')
        max_num = int(re.findall('index_(\d+).html', max_num)[0]) + 1
        if cnum > max_num:
            total = cnum
            break

    total=int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)


    locator = (By.XPATH,'//div[@class="content"][string-length()>40]')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    time.sleep(0.5)
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
    page1 = driver.page_source
    soup1 = BeautifulSoup(page1, 'html.parser')
    div1 = soup1.find('div', class_='content')
    driver.switch_to.frame('iframe')
    try:
        locator=(By.XPATH,'//body[string-length()>10]')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    except:pass
    time.sleep(0.1)
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
    page2 = driver.page_source
    soup2 = BeautifulSoup(page2, 'html.parser')
    div2 = soup2.find('body',class_=False)
    driver.switch_to.parent_frame()


    div = str(div1)+str(div2)
    div = BeautifulSoup(div, 'html.parser')

    return div


data = [

    ["gcjs_zhaobiao_gg", "http://119.164.252.233/jsgl/ztbgl/zbgg/index.html",["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg", "http://119.164.252.233/jsgl/ztbgl/zbgs/index.html",["name", "ggstart_time", "href", "info"], f1, f2],

]

def work(conp, **args):
    est_meta(conp, data=data, diqu="山东省济南市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "lch2", "shandong_jinan"],headless=False,num=1)

    # driver=webdriver.Chrome()
    # df = f3(driver, 'http://119.164.252.233/jsgl/ztbgl/zbgg/201907/t20190702_55494.html')
    # print(df)