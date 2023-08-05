import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import time

from zlsrc.util.etl import est_html, est_meta, add_info



def f1(driver, num):
    locator = (By.XPATH, "//div[@class='left layout2_list_box2']/div[1]/div/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='left page_list_page']/a/font[@color='red']")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        cnum = 1
    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='left layout2_list_box2']/div[1]/div/a").get_attribute('href')[
              -20:]
        driver.execute_script('gopage({})'.format(num))
        locator = (By.XPATH, "//div[@class='left layout2_list_box2']/div[1]/div/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    tbody = soup.find("div", class_='left layout2_list_box2')
    trs = tbody.find_all("div", class_='left layout2_list_row2')
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            title = a['title'].strip()
        except:
            title = a.text.strip()
        href = a['href'].strip()
        if 'http' in href:
            link = href
        else:
            link = 'http://zfcg.xjcz.gov.cn' + a['href'].strip()
        span = tr.find('div', class_='right layout2_list_time').text.strip()
        if re.findall(r'^【(\w+)】', title):
            diqu = re.findall(r'^【(\w+)】', title)[0]
            info = json.dumps({'diqu': diqu}, ensure_ascii=False)
        else:
            info = None
        tmp = [title, span, link, info]
        data.append(tmp)
    df = pd.DataFrame(data)
    return df


def f2(driver):
    locator = (By.XPATH, "//div[@class='left page_list_page']")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='left page_list_page']/a[last()]")
        str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).get_attribute('onclick')
    except:
        num = 1
        return num
    num = int(re.findall(r'(\d+)', str_1)[0])
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@id='counts_info'][string-length()>10]")
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
    div = soup.find('div', id='counts_info')
    return div


data = [
    ["zfcg_gqita_cgxx_gg",
     "http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=143",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'gglx': '采购信息'}), f2],

    ["zfcg_zhaobiao_gg",
     "http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=145",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # #
    ["zfcg_zhongbiao_gg",
     "http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=147",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["zfcg_gqita_bian_cheng_gg",
     "http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=151",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["zfcg_zhaobiao_fscg_gg",
     "http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=149",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '分散采购'}), f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="新疆自治区阿克苏市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "akesu"],pageloadtimeout=120,pageLoadStrategy='none')

    # driver=webdriver.Chrome()
    # url="http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=143"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver=webdriver.Chrome()
    # url="http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=143"
    # driver.get(url)
    # for i in range(3, 5):
    #     df=f1(driver, i)
    #     print(df.values)
    #     for m in df[2].values:
    #         f = f3(driver, m)
    #         print(f)