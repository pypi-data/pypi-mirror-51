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
from zlsrc.util.etl import  est_meta, est_html


def f1(driver, num):
    locator = (By.XPATH, "//div[@class='List1']/ul/li//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # url=driver.current_url
    cnum = int(re.findall("index_([0-9]{1,}).jhtml", driver.current_url)[0])
    if num != cnum:
        url = re.sub("[0-9]{1,}(?=\.jhtml)", str(num), driver.current_url)
        val = driver.find_element_by_xpath("//div[@class='List1']/ul/li[1]//a").get_attribute("href")[-20:]
        driver.get(url)

        locator = (By.XPATH, "//div[@class='List1']/ul/li[1]//a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    div = soup.find("div", class_="List1")
    ul = div.find("ul")
    lis = ul.find_all("li")

    data = []

    for li in lis:
        a = li.find("a", recursive=False)
        ggstart_time = li.find("span").text.strip()
        tmp = [a["title"].strip(), ggstart_time, "http://www.rzggzy.com" + a["href"]]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    try:
        locator = (By.CLASS_NAME, "TxtCenter")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        href = driver.find_element_by_xpath("//div[contains(@class,'TxtCenter'])/div").text

        total = re.findall("共.*\/([0-9]{1,})页", href)[0]
        total = int(total)
    except:
        total = 1
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, "//div[@class='Padding10 BorderCCCDot F14 Contnet'][string-length()>60]")

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))

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

    div = soup.find('div', class_='Center W980 WhiteBg Padding10')
    if div == None: raise ValueError

    return div


data = [

    ["gcjs_zhaobiao_gg", "http://www.rzggzy.com/gjsgc/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_biangeng_gg", "http://www.rzggzy.com/gbggg/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiaohx_gg", "http://www.rzggzy.com/jjsgc/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg", "http://www.rzggzy.com/jcqgg/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangeng_gg", "http://www.rzggzy.com/bzfcg/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiaohx_gg", "http://www.rzggzy.com/jzfcg/index_1.jhtml", ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="河南省汝州市", **args)
    est_html(conp, f=f3, **args)


if __name__ == "__main__":
    work(conp=["postgres", "since2015", "127.0.0.1", "henan", "ruzhou"], num=1, total=2, html_total=10)