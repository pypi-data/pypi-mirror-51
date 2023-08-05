import time
import pandas as pd
import re
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zlsrc.util.etl import add_info,est_meta,est_html,est_tbs




def f1(driver, num):
    locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='pagesite']/div")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', st)[0]

    if num != int(cnum):
        val = driver.find_element_by_xpath("//table[@class='newtable']/tbody/tr[1]/td/a").get_attribute('href')[-15:]
        if num == 1:
            driver.execute_script("location.href=encodeURI('index.jhtml');")
        else:
            driver.execute_script("location.href=encodeURI('index_{}.jhtml');".format(num))

        locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    table= soup.find("table", class_="newtable")
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    data = []
    for tr in trs[:-1]:
        a = tr.find("a")
        if a == None:
            continue
        link = a["href"]
        tds = tr.find_all("td")[2].text
        td = re.findall(r"\[(.*)\]", tds)[0]
        tmp = [a["title"].strip(), td.strip(), link.strip()]
        data.append(tmp)
    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='pagesite']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]
    driver.quit()

    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='newsTex'][string-length()>30]")
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
    div = soup.find('div', class_="newsTex")
    return div


data = [
    ["gcjs_zhaobiao_gg", "http://zw.hainan.gov.cn/ggzy/qhggzy/GGjxzbgs1/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg", "http://zw.hainan.gov.cn/ggzy/qhggzy/GGjxzbgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg", "http://zw.hainan.gov.cn/ggzy/qhggzy/GGZFZBGS/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiaohx_gg", "http://zw.hainan.gov.cn/ggzy/qhggzy/GGZFZBGS1/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]



def work(conp,**args):
    est_meta(conp,data=data,diqu="海南省琼海市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","hainan","qionghai"],ipNum=3,num=4,cdc_total=20,thread_retry=7,headless=True,image_show_gg=2)

