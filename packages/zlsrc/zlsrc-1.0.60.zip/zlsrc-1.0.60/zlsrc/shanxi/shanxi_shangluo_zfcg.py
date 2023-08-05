import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zlsrc.util.etl import est_html, est_meta, add_info



def f1(driver, num):
    locator = (By.XPATH, """//table[@class='class="winstyle1500"']/tbody/tr[2]/td[2]//a | //table[@class='cellspacing="0"']/tbody/tr[2]/td[2]//a""")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//tr[@valign='middle']/td[1]")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    cnum = re.findall(r'(\d+)/', st)[0]
    url = driver.current_url
    if num != int(cnum):
        val = driver.find_element_by_xpath("""//table[@class='class="winstyle1500"']/tbody/tr[2]/td[2]//a | //table[@class='cellspacing="0"']/tbody/tr[2]/td[2]//a""").get_attribute('href')[-30:]

        url = re.sub('(?<=ainfolist\d\d\d\dp=)[0-9]+', str(num), url)
        print(url)
        driver.get(url)

        locator = (By.XPATH, """//table[@class='class="winstyle1500"']/tbody/tr[2]/td[2]//a[not(contains(@href, '%s'))] | //table[@class='cellspacing="0"']/tbody/tr[2]/td[2]//a[not(contains(@href, '%s'))]"""% (val,val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    divs = soup.find("table", class_='class="winstyle1500"')
    if divs==None:
        divs = soup.find("table", class_='cellspacing="0"')
    trs = divs.tbody.find_all("tr")

    data = []
    for tr in trs[1:]:

        tds = tr.find_all('td')[1]
        a=tds.find('a')
        try:
            title = a['title'].strip()
        except:
            title = a.text.strip()
        td = tr.find_all('td')[-1].text.strip()
        link = 'http://www.shangluo.gov.cn'+a['href'].strip()
        tmp = [title, td, link]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, """//table[@class='class="winstyle1500"']/tbody/tr[2]/td[2]//a | //table[@class='cellspacing="0"']/tbody/tr[2]/td[2]//a""")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//tr[@valign='middle']/td[1]")
    st = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    num = re.findall(r'/(\d+)', st)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//table[@width='95%'][string-length()>30]")
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
    div = soup.find('table', width='95%')
    return div


data = [
    ###增加公告
    ["zfcg_zhongbiaohx_gg",
     "http://www.shangluo.gov.cn/zwgk/szfgkmlxxgk.jsp?ainfolist1501t=8&ainfolist1501p=1&ainfolist1501c=15&urltype=egovinfo.EgovInfoList&subtype=1&wbtreeid=1210&sccode=gcztb_zbjg&gilevel=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://www.shangluo.gov.cn/zwgk/szfgkmlxxgk.jsp?ainfolist1501t=8&ainfolist1501p=1&ainfolist1501c=15&urltype=egovinfo.EgovInfoList&subtype=1&wbtreeid=1210&sccode=gcztb_zbgg&gilevel=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ######


    ["zfcg_gqita_zhao_zhong_gg",
     "http://www.shangluo.gov.cn/zwgk/szfgkml.jsp?ainfolist1500t=63&ainfolist1500p=1&ainfolist1500c=15&urltype=tree.TreeTempUrl&wbtreeid=1210",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'zbfs':'公开'}), f2],
]


def work(conp, **args):
    est_meta(conp, data=data, diqu="陕西省商洛市", **args)
    est_html(conp, f=f3, **args)


# 网站新增：http://www.shangluo.gov.cn/zwgk/szfgkml.jsp?urltype=tree.TreeTempUrl&wbtreeid=1210
# 修改时间：2019/8/22
if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "shangluo"], pageloadtimeout=120)

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
        # for j in df[2].values:
        #     df = f3(driver, j)
        #     print(df)