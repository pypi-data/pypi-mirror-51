import json
import math
import re

import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from zlsrc.util.etl import est_html, est_meta, add_info
import time



def f1(driver, num):
    # driver.set_window_size(1366,768)
    locator = (By.XPATH, '//ul[@class="c_ul5"]')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    val = driver.find_element_by_xpath('//ul[@class="c_ul5"]/li[2]/a').get_attribute("href")[-20:]
    cnum = driver.find_element_by_xpath('//p[@class="page"]/label/em').text
    locator = (By.XPATH, '//ul[@class="c_ul5"]/li')
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    if int(cnum) != int(num):
        if 'shtml' not in driver.current_url:
            url = driver.current_url + 'page-'+str(num)+'.shtml'
        else:
            url = re.sub(r'page-\d+','page-%s'%num,driver.current_url)
        # print(url)
        driver.get(url)
        locator = (By.XPATH, '//ul[@class="c_ul5"]/li[2]/a[not(contains(@href,"%s"))]' % val)
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    data = []
    page = driver.page_source
    body = etree.HTML(page)
    content_list = body.xpath('//ul[@class="c_ul5"]/li')[1:]
    for content in content_list:
        name = content.xpath("./a/text()")[0].strip()
        url = content.xpath("./a/@href")[0].strip()
        try:
            mini_text = content.xpath("./p/text()")[0].strip()
        except:mini_text = "None"

        try:
            ggstart_time = re.findall('(\d{4}-\d{2}-\d{2})',mini_text)[0]
        except:ggstart_time = "None"
        info = json.dumps({'mini_text': mini_text}, ensure_ascii=False)
        temp = [name, ggstart_time, url,info]
        data.append(temp)
        # print('temp', temp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    locator = (By.XPATH, '//p[@class="page"]')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    total_page = driver.find_element_by_xpath('//p[@class="page"]/label/span').text
    driver.quit()
    return int(total_page)


def f3(driver, url):
    driver.get(url)
    if "[info]抱歉，请登录或者注册后继续浏览！" in driver.page_source:
        raise ValueError("抱歉，请登录或者注册后继续浏览！")
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
    ["qycg_zhaobiao_gc_gg",
     "https://dfqcgs.dlzb.com/gongcheng/",
     ["name", "ggstart_time", "href","info"], add_info(f1,{"Tag":'工程'}), f2],
    ["qycg_zhaobiao_hw_gg",
     "https://dfqcgs.dlzb.com/huowu/",
     ["name", "ggstart_time", "href","info"], add_info(f1,{"Tag":'货物'}), f2],
    ["qycg_zhaobiao_fw_gg",
     "https://dfqcgs.dlzb.com/fuwu/",
     ["name", "ggstart_time", "href","info"], add_info(f1,{"Tag":'服务'}), f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="东风汽车集团有限公司", **args)
    est_html(conp, f=f3, **args)


if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.3.171", "anbang_qiye", "dfqcgs_dlzb_com"]
    work(conp)
    # for d in data[1:]:
    #
    #     driver = webdriver.Chrome()
    #     url = d[1]
    #     driver.get(url)
    #     df = f1(driver, 2)
    #     print(d[1])
    #     for u in df.values.tolist()[:4]:
    #         print(f3(driver, u[2]))
    #     driver.get(url)
    #
    #     print(f2(driver))
    # driver= webdriver.Chrome()
    # print(f3(driver, 'http://www.ccgp.gov.cn/cggg/zygg/gkzb/201507/t20150701_5493905.htm'))