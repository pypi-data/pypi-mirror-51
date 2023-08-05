import os

import pandas as pd
import re

import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zlsrc.util.fake_useragent import UserAgent

from zlsrc.util.etl import add_info, est_meta, est_html, est_tbs, add_info, est_meta_large
import sys
import time
import json

ua = UserAgent()

proxy = {}

_name_ = 'zlshenpi_hubeisheng'

def get_ip():
    global proxy
    try:
        url = """http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        r = requests.get(url)
        time.sleep(1)
        ip = r.text
        proxy = {'http': ip}
    except:
        proxy = {}
    return proxy


def requests_hb(post_url, post_data):
    global proxy
    if proxy == {}:get_ip()
    try:
        content = requests.post(post_url, data=post_data, headers={"User-Agent": ua.random}, timeout=60, proxies=proxy)
    except:
        proxy = get_ip()
        content = requests.post(post_url, data=post_data, headers={"User-Agent": ua.random}, timeout=60, proxies=proxy)
    return content


def f1(driver, num):
    file_p = os.path.join(os.path.dirname(__file__), 'default_path.txt')
    with open(file_p, 'r') as f: default_path = re.findall('\"([^"]+)\"', f.read())[0]

    locator = (By.XPATH, '//table[@class="index-table"]/tbody/tr[child::td][1]/td')
    val = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text[-24:]

    locator = (By.XPATH, "//a[@class='cur']")
    cnum = int(WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text)
    total = int(driver.find_element_by_xpath('//div[@class="pageNum"]/span[1]/strong').text)
    if num != int(cnum):
        js = """	function goToPage(pageNum){
            if(pageNum > %s){
                alert("请输入正确的页数！");
                return;
            }
            $("#pageNo").val(pageNum);
            $("#publicInformationForm").submit();
            };
            goToPage(%s)
            
            """ % (total, num)
        driver.execute_script(js)
        locator = (By.XPATH, """//table[@class="index-table"]/tbody/tr[child::td][1]/td[not(contains(@onclick, "%s"))]""" % val)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))
    page = driver.page_source
    body = etree.HTML(page)
    contents = body.xpath('//table[@class="index-table"]/tbody/tr[child::td]')

    data = []
    for content in contents:

        if 'queryExamineAll' in driver.current_url:
            name, xm_code = content.xpath("./td[1]/text()|./td[1]/a/text()")

            href_tmp = content.xpath('./td[1]/a')
            if href_tmp != []:
                href = href_tmp[0].xpath('./@onclick')[0].strip()
            else:
                href = "-"
            shixiang = content.xpath('./td[2]/@title')[0].strip()
            shenpi_bumen = content.xpath('./td[3]/text()')[0].strip()
            result = content.xpath('./td[4]/a')

            if result != []:
                if not os.path.exists('%s%s_files/%s.pdf' % (default_path, _name_, xm_code)):
                    sendid = re.findall("\'([^']+)\'", result[0].xpath('./@onclick')[0].strip())[0]
                    url1 = "http://www.hbtzls.gov.cn/portalopenPublicInformation.do?method=downFileBySendid"
                    res1 = requests_hb(url1, {'sendid': sendid}).text
                    res1_dict = json.loads(res1[1:-1])
                    att_uuid = res1_dict['att_uuid']
                    file_path = res1_dict['file_path']
                    att_name = res1_dict['att_name']
                    file_name = res1_dict['file_name']
                    url2 = "http://www.hbtzls.gov.cn/tzxmweb/materialManageHB.do?method=downFileHB"
                    res2 = requests_hb(url2, {"att_uuid": att_uuid, "file_path": file_path, "att_name": att_name, "file_name": file_name}).content
                    if not os.path.exists('%s%s_files' % (default_path, _name_)):os.mkdir('%s%s_files' % (default_path, _name_))
                    with open('%s%s_files/%s.pdf' % (default_path, _name_, xm_code), 'wb') as f:f.write(res2)

            result = content.xpath('./td[4]/a/text()|./td[4]/text()')[0].strip()

            piwenhao = content.xpath('./td[5]/@title')[0].strip()

            ggstart_time = content.xpath('./td[6]/text()')[0].strip()
            info_tmp = {"shixiang": shixiang, 'shenpi_bumen': shenpi_bumen, "xm_code": xm_code, "result": result, "piwenhao": piwenhao}

        else:
            xm_code = content.xpath('./td[1]/text()')[0].strip()
            name = content.xpath('./td[2]/a/@title')[0].strip()
            company = content.xpath('./td[3]/text()')[0].strip()
            ggstart_time = content.xpath('./td[4]/text()')[0].strip()
            shenhe_status = content.xpath('./td[5]/text()')[0].strip()
            shenbao_status = content.xpath('./td[6]/text()')[0].strip()
            try:
                href = content.xpath('./td[2]/a/@onclick')[0].strip()
            except:
                href = "-"
            info_tmp = {"company": company, 'shenhe_status': shenhe_status, "xm_code": xm_code, "shenbao_status": shenbao_status}

        if href == '-':
            info_tmp.update({'hreftype': '不可抓网页'})
        info = json.dumps(info_tmp, ensure_ascii=False)
        tmp = [name, ggstart_time, href, info]
        data.append(tmp)

    df = pd.DataFrame(data)
    return df


def f2(driver):
    locator = (By.XPATH, "//div[@class='pageNum']/span[1]/strong")
    total_page = int(WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text)
    driver.quit()
    return total_page


def f3(driver, url):
    o_url = 'http://www.hbtzls.gov.cn/portalopenPublicInformation.do?method=queryExamineAll'
    if driver.current_url != o_url:
        driver.get(o_url)
    driver.execute_script(url)
    locator = (By.XPATH, '//div[@class="layui-layer-content"] | //div[@class="ucc-info-div"]')
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
    try:
        element = driver.find_element_by_xpath("//a[@class='layui-layer-ico layui-layer-close layui-layer-close1']")
        driver.execute_script("arguments[0].click()", element)
    except:
        pass
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_="layui-layer-content")
    if div == None:
        div = soup.find('div', class_="ucc-info-div")

    return div


data = [
    ["xm_shenpi_gg",
     "http://www.hbtzls.gov.cn/portalopenPublicInformation.do?method=queryExamineAll",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["xm_beian_gg",
     "http://www.hbtzls.gov.cn/tzxmweb/pages/home/approvalResult/recordquery.jsp",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp, **args):
    est_meta_large(conp, data=data, diqu="湖北省", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlshenpi", "hubeisheng"],num=1)
    # for d in data[1:]:
    #     driver=webdriver.Chrome()
        # url=d[1]
        # print(url)
        # driver.get(url)
        # df = f2(driver)
        # print(df)
        # driver = webdriver.Chrome()
        # driver.get(url)
        #
        # df=f1(driver, 12)
        # print(df.values)
        # for f in df[2].values:
        #     d = f3(driver, f)
        #     print(d)
    # driver = webdriver.Chrome()
    # print(f3(driver, """toDetailPage('237c2ba3c43f446296e0c74adc4d33e4','7763ddd4c5244b9ea567c69ab26ade4f','ad52533021a34441a3da8ddac803ef6e','e7b5f00f2d584d0a8d588980373e0836')"""))
