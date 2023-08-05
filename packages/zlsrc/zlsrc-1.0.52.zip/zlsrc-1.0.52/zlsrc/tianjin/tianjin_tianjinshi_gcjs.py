import json

import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from zlsrc.util.etl import  est_meta, est_html, add_info, est_gg,est_meta_large





def f1(driver, num):
    locator = (By.XPATH, '//table[@class="t1"]//tr[2]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=re.findall('Index/(\d+)',url)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath(
            '//table[@class="t1"]//tr[2]//a').get_attribute('href')[-25:]

        url=re.sub('(?<=Index/)\d+',str(num),url)

        driver.get(url)
        locator = (
            By.XPATH, "//table[@class='t1']//tr[2]//a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find("table", class_="t1")
    dls = div.find_all("tr")[1:]

    data = []
    for dl in dls:
        tds = dl.find_all('td')

        name = dl.find('a').get_text().strip()
        href = dl.find('a')['href']
        ggstart_time = tds[-1].get_text().strip()
        procode=tds[2].get_text().strip()
        dw=tds[1].get_text().strip()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.tjconstruct.cn/' + href

        info=json.dumps({'procode':procode,'dw':dw},ensure_ascii=False)

        tmp = [name, ggstart_time, href, info]

        data.append(tmp)
    df = pd.DataFrame(data=data)

    driver.switch_to.parent_frame()
    return df


def f2(driver):
    locator = (By.XPATH, '//table[@class="t1"]//tr[2]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//div[@id="main"]//a[@data-pageindex][last()]').get_attribute('data-pageindex')

    driver.quit()
    return int(total)


def f3(driver, url):
    driver.get(url)

    WebDriverWait(driver,10).until(lambda driver:len(driver.current_url)>=0)

    if '404' in driver.title:
        return '404-找不到文件或目录'
    if '无法找到资源' in driver.title:
        return '无法找到资源'

    locator = (By.XPATH, '//div[@class="body"][string-length()>100] | //div[contains(@class, "Section")]/table[string-length()>50]')
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
        if i > 5:
            break



    # f3 情况1
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_='body')
    if div== None:
        div = soup.find('div', class_=re.compile('Section'))

    if '有效期失效不能访问' in str(div) or div==None:
        raise ValueError


    return div




data=[
    ["gcjs_zhaobiao_shigong_gg" , 'http://www.tjconstruct.cn/Zbgg/Index/2?type=sgzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '施工'}), f2],
    ["gcjs_zhaobiao_jianli_gg" , 'http://www.tjconstruct.cn/Zbgg/Index/2?type=jlzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '监理'}), f2],
    ["gcjs_zhaobiao_sheji_gg" , 'http://www.tjconstruct.cn/Zbgg/Index/2?type=sjzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '设计'}), f2],
    ["gcjs_zhaobiao_shebei_gg" , 'http://www.tjconstruct.cn/Zbgg/Index/2?type=sbzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '设备'}), f2],
    ["gcjs_zhaobiao_zhuanye_gg" , 'http://www.tjconstruct.cn/Zbgg/Index/2?type=qtzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '专业'}), f2],

    ["gcjs_zhongbiao_shigong_gg" , 'http://www.tjconstruct.cn/Zbgs/Index/2?type=sgzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '施工'}), f2],
    ["gcjs_zhongbiao_jianli_gg" , 'http://www.tjconstruct.cn/Zbgs/Index/2?type=jlzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '监理'}), f2],
    ["gcjs_zhongbiao_sheji_gg" , 'http://www.tjconstruct.cn/Zbgs/Index/2?type=sjzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '设计'}), f2],
    ["gcjs_zhongbiao_shebei_gg" , 'http://www.tjconstruct.cn/Zbgs/Index/2?type=sbzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '设备'}), f2],
    ["gcjs_zhongbiao_zhuanye_gg" , 'http://www.tjconstruct.cn/Zbgs/Index/2?type=qtzb', ["name", "ggstart_time", "href", 'info'],add_info(f1, {"gclx": '专业'}), f2],

      ]



def work(conp, **args):
    est_meta_large(conp, data=data, diqu="天津市", **args)
    est_html(conp, f=f3, **args)

# 修改日期：2019/8/15
if __name__ == "__main__":
    # work(
    #     conp=[
    #         "postgres",
    #         "since2015",
    #         '192.168.3.171',
    #         "zhixiashi",
    #         "tianjin"],
    #     headless=False,
    #     num=1,
    # )
    pass
    # driver=webdriver.Chrome()
    # r=f3(driver,'http://tjconstruct.cn/shchxt/tonggao.doc//epr_zbgg/2009/ZBGG0404[2009]0906.htm')
    # print(r)