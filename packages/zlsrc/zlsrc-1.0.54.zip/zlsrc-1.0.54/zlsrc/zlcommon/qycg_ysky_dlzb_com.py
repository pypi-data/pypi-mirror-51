import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

import time

from zlsrc.util.etl import est_html, est_meta, add_info,est_meta_large



def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='c_ul5']/li[last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    try:
        locator = (By.XPATH, "//p[@class='page']/label/em")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        cnum = 1
    if num != int(cnum):
        val = driver.find_element_by_xpath("//ul[@class='c_ul5']/li[2]/a").get_attribute('href')[-15:]
        tar = driver.find_element_by_xpath("//ul[@class='c_ul5']/li[last()]/a").get_attribute('href')[-15:]
        if "page" not in url:
            s = "page-%d.shtml" % (num) if num > 1 else ""
            url += s
        elif num == 1:
            url = re.sub("page-[0-9]*\.shtml", "", url)
        else:
            s = "page-%d.shtml" % (num) if num > 1 else ""
            url = re.sub("page-[0-9]*\.shtml", s, url)
        driver.get(url)

        locator = (By.XPATH, "//ul[@class='c_ul5']/li[2]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//ul[@class='c_ul5']/li[last()]/a[not(contains(@href, '%s'))]" % tar)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find("ul", class_='c_ul5')
    div.find('p', class_='page').extract()
    lis = div.find_all('li')
    data = []
    for li in lis[1:]:
        a = li.find("a")
        try:
            title = a['title'].strip()
        except:
            title = a.text.strip()
        link = a["href"]
        if 'http' in link:
            href = link
        else:
            href = 'https://www.dlzb.com/' + link
        if li.find('p'):
            txt = li.find('p').text.strip()
            info = json.dumps({'pinfo':txt}, ensure_ascii=False)
            span = '-'
        else:
            span = '-'
            info = None

        tmp = [title, span, href, info]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@class='c_ul5']/li[2]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//p[@class='page']/label/span")
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        num = 1
    driver.quit()
    return int(num)

def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@id='content'][string-length()>100]")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
    before = len(driver.page_source)
    time.sleep(1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.5)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div= soup.find('div', id="content").parent

    if div.name == 'div' and div.get('class') == None:
        div = div.parent

    return div


data = [
    ["qycg_gqita_zhao_bian_hw_gg",
     "https://ysky.dlzb.com/huowu/",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],

    ["qycg_gqita_zhao_bian_gc_gg",
     "https://ysky.dlzb.com/gongcheng/",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'工程'}), f2],

    ["qycg_gqita_zhao_bian_fw_gg",
     "https://ysky.dlzb.com/fuwu/",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
]


def work(conp, **args):
    est_meta(conp, data=data, diqu="中国有色矿业集团有限公司", **args)
    est_html(conp, f=f3, **args)


# 该网站需要登录才能看到更多数据，详情页无法全部获取完
if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang3", "ysky_dlzb_com"])

    # driver = webdriver.Chrome()
    # url = "https://ysky.dlzb.com/fuwu/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # driver=webdriver.Chrome()
    # url = "https://ysky.dlzb.com/fuwu/"
    # driver.get(url)
    # for i in range(11, 13):
    #     df=f1(driver, i)
    #     print(df.values)
    #     for i in df[2].values:
    #         f = f3(driver, i)
    #         print(f)
