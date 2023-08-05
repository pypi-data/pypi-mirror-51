

import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

from zlsrc.util.etl import est_html, est_meta





def f1(driver, num):
    url = driver.current_url
    locator = (By.XPATH, "//div[@class='list_right']/ul/li[last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='pagination_index_num currentIndex']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = int(str)
    except:
        cnum = 1

    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='list_right']/ul/li[last()]/a").get_attribute('href')[-30:]

        if "list_" not in url:
            s = "list_%d" % (num) if num > 1 else "list"
            url = re.sub("list", s, url)
        elif num == 1:
            url = re.sub("list_[0-9]*", "list", url)
        else:
            s = "list_%d" % (num) if num > 1 else "list"
            url = re.sub("list_[0-9]*", s, url)
        driver.get(url)
        locator = (By.XPATH, "//div[@class='list_right']/ul/li[last()]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find("div", class_="list_right").ul
    trs = div.find_all("li")
    data = []
    for tr in trs:
        a = tr.find('a')
        name = a.text.strip()
        ggstart_time = tr.find('span').text.strip()
        href = 'http://www.shantou.gov.cn' + a['href'].strip()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info']= None
    return df


def f2(driver):
    locator = (By.XPATH, "//div[@class='list_right']/ul/li[last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='pag_cout']")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    num = re.findall(r'共 (\d+) 页', st)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='cen-main'][string-length()>40]")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
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
    div = soup.find('div', class_='cen-main')
    return div


data = [
    ["zfcg_gqita_liu_zhongbhx_gg", "http://www.shantou.gov.cn/cnst/yzbgg/list.shtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["zfcg_zhaobiao_gg", "http://www.shantou.gov.cn/cnst/cggg/list.shtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangeng_gg", "http://www.shantou.gov.cn/cnst/gzgg/list.shtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg", "http://www.shantou.gov.cn/cnst/zbgg/list.shtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]

###汕头市人民政府
def work(conp, **args):
    est_meta(conp, data=data, diqu="广东省汕头市", **args)
    est_html(conp, f=f3, **args)


# 网站新增：http://www.shantou.gov.cn/cnst/zfcg/list.shtml
# 修改时间：2019/6/20
if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "shantou"])

    # driver = webdriver.Chrome()
    # for d in data:
    #     driver.get(d[1])
    #     print(d[1])
    #     df = f2(driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(d[1])
    #     df = f1(driver,3)
    #     print(df.values)
    #     for j in df[2].values:
    #         df = f3(driver, j)
    #         print(df)