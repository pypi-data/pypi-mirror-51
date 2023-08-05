import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from zlsrc.util.etl import est_tbs, est_meta, est_html, add_info,est_meta_large



def f1(driver, num):
    locator = (By.XPATH, '//ul[@class="c_ul5"]/li[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    page_num = re.findall('page-(\d+?)\.shtml', url)
    cnum = 1 if not page_num else page_num[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//ul[@class="c_ul5"]/li[2]/a').get_attribute('href')[-20:-5]
        if num == 1:
            url = url.rsplit('/', maxsplit=1)[0]
        else:
            url = re.sub('page-\d+.shtml', 'page-%d.shtml' % num, url)
        driver.get(url)

        locator = (By.XPATH, '//ul[@class="c_ul5"]/li[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', class_='c_ul5')
    trs = div.find_all('li', recursive=False)[1:]
    for tr in trs:
        name = tr.a.get_text()
        href = tr.a['href']
        ggstart_time = 'kong'

        if 'http' in href:
            href = href
        else:
            href = 'https://sytrq.dlzb.com/' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)

    df = pd.DataFrame(data=data)
    df["info"] = None

    return df


def f2(driver):

    locator = (By.XPATH, '//ul[@class="c_ul5"]/li[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//p[@class="page"]/a[last()]').get_attribute('href')
    total = re.findall('page-(\d+?).shtml', total)[0]

    total = int(total)

    driver.quit()

    return total




def f3(driver, url):
    driver.get(url)


    locator = (By.XPATH,
               '//div[@id="content"][string-length()>200]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

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
        if i > 10: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    div = soup.find('div', id="content").parent
    if div.name == 'div' and div.get('class') == None:
        div=div.parent

    return div


data = [

    ["qycg_gqita_zhao_zhong_gongcheng_gg", "https://syhggs.dlzb.com/gongcheng/page-2.shtml",["name", "ggstart_time", "href", "info"],add_info(f1,{"gclx":'工程'}), f2],
    ["qycg_gqita_zhao_zhong_huowu_gg", "https://syhggs.dlzb.com/huowu/page-2.shtml",["name", "ggstart_time", "href", "info"], add_info(f1,{"gclx":'货物'}), f2],
    ["qycg_gqita_zhao_zhong_fuwu_gg", "https://syhggs.dlzb.com/fuwu/page-2.shtml",["name", "ggstart_time", "href", "info"],add_info(f1,{"gclx":'服务'}), f2],

]


def work(conp, **args):
    est_meta_large(conp, data=data, diqu="中国石油化工集团", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    # work(conp=["postgres", "since2015", "192.168.3.171", "lch3", "syhggs_dlzb_com"],headless=False)
    pass
    driver=webdriver.Chrome()
    f3(driver,'https://www.dlzb.com/d-zb-3773740.html')