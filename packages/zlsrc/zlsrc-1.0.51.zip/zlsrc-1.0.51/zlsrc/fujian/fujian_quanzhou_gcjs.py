import time
import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from zlsrc.util.etl import est_tbs, est_meta, est_html



def f1(driver, num):

    locator = (By.XPATH, '//div[@class="qyyb"]/table[2]//tr[2]/td[2]/a')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located(locator))

    url = driver.current_url
    cnum = re.findall('page=(\d+)', url)[0]

    if cnum != str(num):
        val = driver.find_element_by_xpath('//div[@class="qyyb"]/table[2]//tr[2]/td[2]/a').get_attribute('onclick')

        url = url.rsplit('=', maxsplit=1)[0] + '=%s' % num
        driver.get(url)
        locator = (By.XPATH, '//div[@class="qyyb"]/table[2]//tr[2]/td[2]/a[not(contains(@onclick,"{}"))]'.format(val))
        WebDriverWait(driver, 40).until(EC.presence_of_element_located(locator))

    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('div', class_="qyyb").find_all('table')[1].find_all('tr')[1:]

    for tr in trs:
        tds = tr.find_all('td')
        index_num = tds[0]['title']
        href = tds[1].a['onclick']
        name = tds[1].a['title']
        jsdw = tds[2].get_text().strip()
        ggstart_time = tds[3].get_text().strip()

        href = re.findall("OpenWin\('(.+?)',", href)[0]

        if 'http' in href:
            href = href
        else:
            href = 'http://www.qzzb.gov.cn:8888/' + href
        info={'index_num':index_num,'jsdw':jsdw}
        info=json.dumps(info,ensure_ascii=False)

        tmp = [name, ggstart_time, href,info]

        data.append(tmp)
    df = pd.DataFrame(data=data)

    return df

def f2(driver):
    locator = (By.XPATH, '//div[@class="qyyb"]/table[2]//tr[2]/td[2]/a')
    WebDriverWait(driver, 40).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//div[@class="db"]/span').text
    total = re.findall('共 (\d+?) 页', total)[0].strip()

    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH,
               '//body[string-length()>20]')

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))

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

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    div = soup.find('body')

    if '有效期失效不能访问' in str(div):
        raise ValueError

    return div


data = [
    #包含所有
    ["gcjs_gqita_zhao_zhong_gg", "http://www.qzzb.gov.cn:8888/zbxx_zbgc.asp?scid=1&centerID=&PrjType=&ProjNo=&ProjName=&OwnerDeptName=&page=1",["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="福建省泉州市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "lch2", "fujian_quanzhou"],pageLoadStrategy='none',pageloadtimeout=60,headless=False,num=1)