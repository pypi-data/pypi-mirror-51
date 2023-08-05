import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import json
from zlsrc.util.etl import add_info,est_meta,est_html,est_tbs




def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='ewb-list']/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@id='index']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = str.split('/')[0]
    except:
        cnum = 1

    url = driver.current_url
    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@id='categorypagingcontent']/ul[@class='ewb-list']/li[1]/a").get_attribute('href')[-30:]
        if "subPage" in url:
            s = "/%d.html" % (num) if num > 1 else "/1.html"
            url = re.sub("/subPage_jyxx\.html", s, url)
        elif num == 1:
            url = re.sub("/[0-9]*\.html", "/1.html", url)
        else:
            s = "/%d.html" % (num) if num > 1 else "/1.html"
            url = re.sub("/[0-9]*\.html", s, url)

        driver.get(url)
        locator = (By.XPATH, "//div[@id='categorypagingcontent']/ul[@class='ewb-list']/li[1]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("div", id='categorypagingcontent')
    ul = table.find("ul", class_='ewb-list')
    trs = ul.find_all("li")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()
        try:
            link = a["href"]
        except:
            link = '-'
        span = tr.find("span", class_="ewb-list-date").text.strip()
        links = "http://www.sxggzyjy.cn"+link.strip()
        tmp = [title, span, links]
        data.append(tmp)
    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@class='ewb-list']/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@id='index']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = str.split('/')[1]
    except:
        num = 1
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='ewb-main'][string-length()>40]")
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
    div = soup.find('div', class_="ewb-main")
    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001001/001001001001/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["gcjs_gqita_bian_cheng_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001001/001001001002/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["gcjs_gqita_liu_zhongz_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001001/001001001004/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001001/001001001005/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["gcjs_zhongbiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001001/001001001003/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001004/001001004001/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangeng_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001004/001001004002/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001004/001001004003/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["zfcg_gqita_liu_zhongz_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001004/001001004004/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    #
    ["yiliao_zhaobiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001006/001001006001/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'jylx':'医用药品耗材及医疗机械采购'}), f2],
    #
    ["yiliao_gqita_yaopin_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001006/001001006003/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"],add_info(f1,{'jylx':'医用药品耗材及医疗机械采购','gglx':'药品公示公告'}), f2],
    #
    ["yiliao_gqita_haocai_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001006/001001006004/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"],add_info(f1,{'jylx':'医用药品耗材及医疗机械采购','gglx':'耗材公示公告'}), f2],

    ["qsy_zhaobiao_gg",
     "http://www.sxggzyjy.cn/jydt/001001/001001012/001001012001/subPage_jyxx.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'jylx':'其他'}), f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="陕西省",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","shanxi","shenghui"])

