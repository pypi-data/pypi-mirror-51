import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import json
from zlsrc.util.etl import add_info,est_meta,est_html




def f1(driver, num):
    locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', st)[0]
    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='Right-Border floatL']/dl/dt[1]/a").get_attribute('href')[-12:]
        if 'index.htm' in url:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub('index', s, url)
        elif num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)
        driver.get(url)
        locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div= soup.find("div", class_='Right-Border floatL')
    trs = div.find_all("dt")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()
        if '\n' in title:
            title = title.split('\n')[0]
        try:
            link = a["href"]
        except:
            link = '-'
        span = tr.find("span").text
        span = re.findall(r'\[(.*)\]', span)[0]
        if 'http' in link:
            link = link.strip()
        else:
            link = "http://ggzyjy.dongyang.gov.cn" + link.strip()
        info = {}
        if re.findall(r'^\[(.*?)\]', title):
            diqu = re.findall(r'^\[(.*?)\]', title)[0]
            info['diqu'] = diqu
        if a.find('label'):
            if ('/xzzbgg/' in url) or ('/dybcgg/' in url) or ('/pbjggs/' in url):
                lx = a.find('label').text.strip()
                lx = re.findall(r'(\w+)', lx)[0]
                info['lx'] = lx
            else:
                zblx = a.find('label').text.strip()
                zblx = re.findall(r'(\w+)', zblx)[0]
                info['zblx'] = zblx
        if info:info = json.dumps(info, ensure_ascii=False)
        else:info = None
        tmp = [title, span.strip(), link, info]
        data.append(tmp)
    df = pd.DataFrame(data)
    return df



def f2(driver):
    url = driver.current_url
    locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', st)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    time.sleep(1)
    if '404' in driver.title:
        return 404
    if "http://www.zjzfcg.gov.cn/" in url:
        locator = (By.XPATH, "//div[@class='gpoz-detail-content'][string-length()>100]")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        if 'id="detail_frame' in str(driver.page_source):
            page1 = driver.page_source
            soup1 = BeautifulSoup(page1, 'html.parser')
            div1 = soup1.find('div', class_='gpoz-detail-content')
            driver.switch_to_frame('detail_frame')
            locator = (By.XPATH, "//div[@id='iframe_box'][string-length()>100]")
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
            before = len(driver.page_source)
            time.sleep(0.5)
            after = len(driver.page_source)
            i = 0
            while before != after:
                before = len(driver.page_source)
                time.sleep(0.1)
                after = len(driver.page_source)
                i += 1
                if i > 5: break
            page2= driver.page_source
            soup2 = BeautifulSoup(page2, 'html.parser')
            div2 = soup2.find('body')
            div = str(div1)+str(div2)
            div = BeautifulSoup(div, 'html.parser')
            return div

        locator = (By.XPATH, "//div[@class='detail-content'][string-length()>100]")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
        before = len(driver.page_source)
        time.sleep(1)
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
        div = soup.find('div', class_='gpoz-detail-content')
        return div
    else:
        locator = (By.XPATH, "//div[@class='Main-p floatL'][string-length()>100]")
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
        before = len(driver.page_source)
        time.sleep(1)
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
        div = soup.find('div', class_='content-Border floatL')
        return div


data = [
    ["gcjs_zhaobiao_gg","http://ggzyjy.dongyang.gov.cn/jsgcgcjszbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gqita_bian_da_gg", "http://ggzyjy.dongyang.gov.cn/jsgcgcjsdycq/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg", "http://ggzyjy.dongyang.gov.cn/jsgcgcjspbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg", "http://ggzyjy.dongyang.gov.cn/jsgcgcjszbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg", "http://ggzyjy.dongyang.gov.cn/zfcgggyg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg", "http://ggzyjy.dongyang.gov.cn/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gqita_zhong_zhongz_gg", "http://ggzyjy.dongyang.gov.cn/zfcgzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg", "http://ggzyjy.dongyang.gov.cn/zfcgzbhxgs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_hetong_gg", "http://ggzyjy.dongyang.gov.cn/zfcghtgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsy_zhaobiao_gg", "http://ggzyjy.dongyang.gov.cn/xzzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],add_info(f1, {'jylx':'乡镇招投标'}),f2],

    ["qsy_gqita_bian_da_gg", "http://ggzyjy.dongyang.gov.cn/dybcgg/index.htm",
     ["name", "ggstart_time", "href", "info"],add_info(f1, {'jylx':'乡镇招投标'}),f2],

    ["qsy_gqita_zhonghx_liu_gg", "http://ggzyjy.dongyang.gov.cn/pbjggs/index.htm",
     ["name", "ggstart_time", "href", "info"],add_info(f1, {'jylx':'乡镇招投标'}),f2],
]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省东阳市",**args)
    est_html(conp,f=f3,**args)

# 修改日期：2019/7/8
if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","dongyang"],pageloadtimeout=120)


    # for d in data[9:]:
    #     driver=webdriver.Chrome()
    #     url=d[1]
    #     print(url)
    #     driver.get(url)
    #     df = f2(driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #
    #     df=f1(driver, 3)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)
    # driver = webdriver.Chrome()
    # df = f3(driver, 'http://ggzyjy.dongyang.gov.cn/jsgcgcjszbjg/18598.htm')
    # print(df)
