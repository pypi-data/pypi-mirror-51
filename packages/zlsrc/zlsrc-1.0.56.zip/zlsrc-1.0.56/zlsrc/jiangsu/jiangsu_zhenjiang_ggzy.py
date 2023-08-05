import json
import math
import random
import re
from bs4 import BeautifulSoup
from lmfscrap import web
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from zlsrc.util.etl import  est_meta, est_html,add_info
from zlsrc.util.fake_useragent import UserAgent
import requests
import time




ua=UserAgent()
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'ggzy.zhenjiang.gov.cn',
    'Referer': 'http://ggzy.zhenjiang.gov.cn/jyxx/001005/001005004/second-page.html',
    'User-Agent': ua.chrome
}

proxy = {}


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

def f3(driver, url):
    driver.get(url)
    time.sleep(0.2)
    if '404 Not Found' in driver.page_source:
        return '404 Not Found'
    locator = (By.CLASS_NAME, "article-block")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator))

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
    div = soup.find('div', class_='article-block')
    return div


def f1(driver, num):
    url = re.sub("pageIndex=\d+","pageIndex="+str(num),driver.current_url)
    driver_info = webdriver.DesiredCapabilities.CHROME
    try:
        if "--proxy" in driver_info['goog:chromeOptions']['args'][0]:
            proxy_ip = driver_info['goog:chromeOptions']['args'][0].split('=')[1].split('://')
            proxies = {proxy_ip[0]: proxy_ip[1]}
            page_temp = requests.get(url, proxies=proxies, headers=headers,timeout=40).text
        else:
            if proxy == {}: get_ip()
            page_temp = requests.get(url, headers=headers,timeout=40,proxies=proxy).text
    except:
        try:
            page_temp = requests.get(url, headers=headers,timeout=40,proxies=proxy).text
        except:
            get_ip()
            page_temp = requests.get(url, headers=headers, timeout=40, proxies=proxy).text
    page = json.loads(page_temp)["return"]
    content_list = json.loads(page).get('Table')
    data = []
    # print(content_list)
    for content in content_list:
        name = content.get("title")
        ggstart_time = content.get("infodate")
        url = "http://ggzy.zhenjiang.gov.cn" + content.get("infoUrl")
        temp = [name, ggstart_time, url]

        data.append(temp)
        # print(temp)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df


def f2(driver):
    categorynum = re.findall(r'categorynum=(\d+)',driver.current_url)[0]

    page_size = int(re.findall(r'pageSize=(\d+)',driver.current_url)[0])
    count_url = re.sub(r'categorynum=(\d+)','categorynum='+categorynum,"http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubByCount?response=application/json&categorynum=001001002001&title=")

    total_item = int(json.loads(requests.get(count_url,timeout=40).text).get('return'))
    total_page = math.ceil(total_item/page_size)

    driver.quit()
    return total_page


data = [

    ["gcjs_zhaobiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_zhaobiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_zhaobiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_zhaobiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_zhaobiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    ["gcjs_zhaobiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],

    ["gcjs_zsjg_weiruwei_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_zsjg_weiruwei_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_zsjg_weiruwei_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    ["gcjs_zsjg_weiruwei_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],


    ["gcjs_zhongbiaohx_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_zhongbiaohx_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_zhongbiaohx_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_zhongbiaohx_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_zhongbiaohx_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    ["gcjs_zhongbiaohx_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],



    ["gcjs_zhongbiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_zhongbiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_zhongbiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_zhongbiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_zhongbiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    ["gcjs_zhongbiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],



    ["gcjs_biangeng_pmchange_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_biangeng_pmchange_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_biangeng_pmchange_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006003&title=",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_biangeng_pmchange_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_biangeng_pmchange_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    ["gcjs_biangeng_pmchange_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],




####


    ["gcjs_jiaotong_zhaobiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_jiaotong_zhaobiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_jiaotong_zhaobiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_jiaotong_zhaobiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_jiaotong_zhaobiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],

    ["gcjs_jiaotong_zhongbiao_shiqu_gg","http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_jiaotong_zhongbiao_danyang_gg","http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_jiaotong_zhongbiao_jvrong_gg","http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_jiaotong_zhongbiao_yangzhong_gg","http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_jiaotong_zhongbiao_dantu_gg","http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],




#
    ["gcjs_shuili_zhaobiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_shuili_zhaobiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_shuili_zhaobiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_shuili_zhaobiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["gcjs_shuili_zhaobiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_shuili_zhaobiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
#
#
    ["gcjs_shuili_zhongbiaohx_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_shuili_zhongbiaohx_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_shuili_zhongbiaohx_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_shuili_zhongbiaohx_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["gcjs_shuili_zhongbiaohx_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_shuili_zhongbiaohx_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    #
    ["gcjs_shuili_zhongbiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["gcjs_shuili_zhongbiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["gcjs_shuili_zhongbiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["gcjs_shuili_zhongbiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"})     , f2],
    ["gcjs_shuili_zhongbiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["gcjs_shuili_zhongbiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
#
    #
    ["zfcg_zhaobiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["zfcg_zhaobiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["zfcg_zhaobiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["zfcg_zhaobiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["zfcg_zhaobiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["zfcg_zhaobiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
    #
    ["zfcg_biangeng_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["zfcg_biangeng_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["zfcg_biangeng_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["zfcg_biangeng_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["zfcg_biangeng_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["zfcg_biangeng_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
#    #
    ["zfcg_zhongbiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["zfcg_zhongbiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["zfcg_zhongbiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["zfcg_zhongbiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["zfcg_zhongbiao_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["zfcg_zhongbiao_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],#
    #
    ["zfcg_dyly_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["zfcg_dyly_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["zfcg_dyly_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["zfcg_dyly_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],
    ["zfcg_dyly_yangzhong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"扬中"}), f2],
    ["zfcg_dyly_dantu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005005&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹徒"}), f2],
#
    ["jqita_gqita_zhao_zi_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005001001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["jqita_gqita_zhao_zi_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005001003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["jqita_gqita_zhao_zi_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005001006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],

    ["jqita_zhongbiao_shiqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002001&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江市区"}), f2],
    ["jqita_zhongbiao_danyang_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002002&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"丹阳"}), f2],
    ["jqita_zhongbiao_jvrong_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"句容"}), f2],
    ["jqita_zhongbiao_xinqu_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002006&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"area":"镇江新区"}), f2],

    ["jqita_zhaobiao_jun_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005003&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"attr":"涉及军队"}), f2],
    ["jqita_gqita_zhong_liu_jun_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005004&title=",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{"attr":"涉及军队"}), f2],

    ["yiliao_zhaobiao_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001008001001&title=",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["yiliao_zhongbiao_gg", "http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001008002001&title=",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**kwargs):
    est_meta(conp, data=data, diqu="江苏省镇江市",**kwargs)
    est_html(conp, f=f3,**kwargs)


if __name__ == "__main__":

    conp=["postgres", "since2015", "192.168.3.171", "jiangsu", "zhenjiang"]
    work(conp,num=3,total=10)
