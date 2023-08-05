import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from zlsrc.util.etl import est_html, est_meta, add_info



def f1(driver, num):
    locator = (By.XPATH, "//div[@class='list-container']/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//li[@class='paginationjs-page J-paginationjs-page active']/a")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        cnum = 1
    url = driver.current_url
    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='list-container']/ul/li[1]/a").get_attribute('href')[-30:]
        locator = (By.XPATH, "//input[@class='J-paginationjs-go-pagenumber']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, "//input[@class='J-paginationjs-go-pagenumber']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
        locator = (By.XPATH, "//div[@class='list-container']/ul/li[1]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    ul = soup.find("div", class_="list-container").ul
    trs = ul.find_all("li")
    data = []
    for tr in trs:
        info = {}
        a = tr.find('a')
        if a.find('span', class_="district"):
            tal = a.find('span', class_="district").extract().text.strip()
            if re.findall(r'\[(.*)\]', tal):
                tt = re.findall(r'\[(.*)\]', tal)[0]
                if '·' in tt:
                    diqu = tt.split('·', maxsplit=1)[0]
                    lx = tt.split('·', maxsplit=1)[1]
                    info['diqu'] = diqu
                    info['lx'] = lx
        try:
            title = a['title'].strip()
        except:
            title = a.text.strip()
        td = tr.find('span', class_="date").text.strip()
        link = a['href'].strip()
        if 'http' in link:
            href = a['href'].strip()
        else:
            href = 'http://www.ccgp-xinjiang.gov.cn' + link
        if info:
            info = json.dumps(info, ensure_ascii=False)
        else:
            info = None
        tmp = [title, td, href, info]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    url = driver.current_url
    if '暂无数据' in str(driver.page_source):
        return 0
    try:
        locator = (By.XPATH, "//div[@class='list-container']/ul/li[1]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//li[@class='paginationjs-page paginationjs-last J-paginationjs-page']/a")
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        if '暂无数据' in str(driver.page_source):
            return 0
        locator = (By.XPATH, "//div[@class='list-container']/ul/li[1]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        num = 1
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    if '<iframe id="iframe' in driver.page_source:
        driver.switch_to_frame('iframe')
    locator = (By.XPATH,
               "//body[@class='view'][string-length()>10] | //div[@class='artcl_m'][string-length()>10] | //div[@class='right_con'][string-length()>10]")
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
    div = soup.find('body', class_='view')
    if div == None:
        div = soup.find('div', class_='artcl_m')
        if div == None:
            div = soup.find('div', class_='right_con')
    return div


data = [
    ["zfcg_zhaobiao_gk_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3001/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '公开招标'}), f2],

    ["zfcg_zhaobiao_jztp_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3002/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '竞争性谈判'}), f2],

    ["zfcg_zhaobiao_xj_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3003/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '询价'}), f2],

    ["zfcg_zhaobiao_yq_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3008/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '邀请招标'}), f2],

    ["zfcg_zhaobiao_jzcs_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3011/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '竞争性磋商'}), f2],

    ["zfcg_zgys_gk_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement2001/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '公开招标'}), f2],

    ["zfcg_yucai_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/ZcyAnnouncement3014/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_jkcp_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/ZcyAnnouncement3013/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '进口产品'}), f2],

    ["zfcg_dyly_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/ZcyAnnouncement3012/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["zfcg_zhongbiao_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement4/ZcyAnnouncement3004/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zgysjg_yq_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement4/ZcyAnnouncement3009/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '邀请招标'}), f2],

    ["zfcg_zhongzhi_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement4/ZcyAnnouncement3015/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_gqita_jieguobiangeng_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement4/ZcyAnnouncement3017/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'gglx': '采购结果变更公告'}), f2],

    ["zfcg_zgysjg_gk_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement4/ZcyAnnouncement4004/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs': '公开招标'}), f2],

    #
    ["zfcg_hetong_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement5/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    #
    ["zfcg_biangeng_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement3/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_liubiao_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement10/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yanshou_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement6/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_gqita_zhao_zhong_dianzi_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement8/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'gglx': '电子卖场公告'}), f2],

    ["zfcg_gqita_feigongkai_gg",
     "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement9/index.html",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zblx': '非公开'}), f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="新疆自治区", **args)
    est_html(conp, f=f3, **args)


# 网址变更
if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "xinjiang2"], pageloadtimeout=120,headless=False,num=1)

    # driver=webdriver.Chrome()
    # url = "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/ZcyAnnouncement3013/index.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver=webdriver.Chrome()
    # url = "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/ZcyAnnouncement3013/index.html"
    # driver.get(url)
    # for i in range(2, 5):
    #     df=f1(driver, i)
    #     print(df.values)
    #     for d in df[2].values:
    #         f =f3(driver, d)
    #         print(f)
