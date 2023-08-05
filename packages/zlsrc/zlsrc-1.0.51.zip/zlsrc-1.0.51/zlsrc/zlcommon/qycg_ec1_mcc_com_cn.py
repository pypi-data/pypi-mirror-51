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
from zlsrc.util.etl import est_html, est_meta, est_meta_large
import time



def f1(driver, num):
    locator = (By.XPATH, '//table[@class="datatlb"]/tbody/tr')
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    val = driver.find_element_by_xpath('//table[@class="datatlb"]/tbody/tr[2]/td/a').text
    cnum = driver.find_element_by_xpath("//input[@id='input_page']").get_attribute("value")
    if int(cnum) != int(num):
        driver.execute_script("javascript:queryData(%s)" % num)
        locator = (By.XPATH, '//table[@class="datatlb"]/tbody/tr[2]/td/a[not(contains(text(),"%s"))]' % val)
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    page = driver.page_source
    body = etree.HTML(page)
    data = []
    content_list = body.xpath('//table[@class="datatlb"]/tbody/tr')[1:]
    for content in content_list:
        name = content.xpath("./td/a/text()")[0].strip()
        ggstart_time = content.xpath("./td[2]/text()")[0].strip()
        url_list = content.xpath("./td/a/@onclick | ./td/a/@href")
        if url_list[0] == '#':
            url_temp = re.findall('\'([^\']+)\'', url_list[1])[0]
        else:
            url_temp = re.findall('\'([^\']+)\'', url_list[0])[0]

        if "当前信息供应商登录后才能查看！" in url_temp:
            # 需要登录才能查看
            url = "当前信息供应商登录后才能查看！"

        elif 'showCgxjMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showCgxjDetail&xjbm="+url_temp

        elif 'showMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showMessage&xxbh="+url_temp

        elif 'showZgysDetail' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showZgysDetail&zgyswjbm="+url_temp

        elif 'toShowAbout' in ''.join(url_list):

            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=aboutUs"

        elif 'showNouseDepartmentMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + '/b2b/web/two/indexinfoAction.do?actionType=showNouseDepartmentDetail&sbbm=' + url_temp

        elif 'showCgxjMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showCgxjDetail&xjbm=" + url_temp

        elif 'showZbsMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showZbsDetail&inviteid=" + url_temp

        elif 'showCgwzMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showUrgentDetail&xxbh=" + url_temp

        elif 'showWxwzMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showSaleDetail&xxbh=" + url_temp

        elif 'showOldMaterialMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showOldMaterialDetail&xxbh=" + url_temp

        elif 'showInvalidMaterialMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showInvalidMaterialDetail&xxbh=" + url_temp

        elif 'showXcpMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showNewProductDetail&dwbm=" + url_temp + "&xh==undefined"


        elif 'showYzbgsMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showYzbgsDetail&xxbh=" + url_temp + "&inviteid==undefined"
        #

        elif 'showZhongbggMessage' in ''.join(url_list):

            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showZhongbggDetail&xxbh=" + url_temp + "&inviteid=undefined"


        elif 'showCqggMessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showCqggDetail&xxbh=" + url_temp

        elif 'showPxjgmessage' in ''.join(url_list):
            url = 'http://ec1.mcc.com.cn' + "/b2b/web/two/indexinfoAction.do?actionType=showPxjgDetail&xxbh=" + url_temp

        temp = [name, ggstart_time, url]
        data.append(temp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//td[@width="150"]')))
    total_page = re.findall(r'\/ (\d+)', driver.find_element_by_xpath('//td[@width="150"]').text)[0]
    driver.quit()
    return int(total_page)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, '//div[@class="main-news"]')
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located(locator))

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
    if len(page) <= 3212:
        return '页面无内容。'
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_="main-news")

    return div


data = [
    ["qycg_zhaobiao_1_gg",
     "http://ec1.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showMoreCgxx&xxposition=cgxx",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["qycg_zhaobiao_gg",
     "http://ec1.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showMoreZbs&xxposition=zbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["qycg_biangeng_gg",
     "http://ec1.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showMoreClarifypub&xxposition=cqgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["qycg_zhongbiao_gg",
     "http://ec1.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showMorePub&xxposition=zhongbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]

##中国五矿集团有限公司采购电子商务平台
def work(conp, **args):
    est_meta_large(conp, data=data, diqu="中国五矿集团", **args)
    est_html(conp, f=f3, **args)


if __name__ == "__main__":
    # conp = ["postgres", "since2015", "192.168.3.171", "anbang_qiye", "ec1_mcc_com_cn"]
    # work(conp,pageloadstrategy='none',pageloadtimeout=30)
    for i in data:
        driver = webdriver.Chrome()
        driver.get(i[1])
        df = f1(driver, 2).values.tolist()
        print(df)
        for d in df[:2]:
            print(f3(driver, d[2]))
        driver.get(i[1])
        print(f2(driver))
