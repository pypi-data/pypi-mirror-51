import time

from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from zlsrc.util.etl import est_meta,est_html

def f1(driver,num):
    locator = (By.XPATH,'//*[@id="MoreInfoList1_DataGrid1"]//a')
    WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located(locator))
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]//tr[1]//a').get_attribute("href")[-50:]
    cnum = driver.find_element_by_xpath("//div[@id='MoreInfoList1_Pager']//font[@color='red']").text
    if int(cnum) != int(num):
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','%s')"%num)
        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]//tr[1]//a[not(contains(@href,"%s"))]'%val)
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    page = driver.page_source
    body = etree.HTML(page)
    data = []
    content_list = body.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr')
    for content in content_list:
        name = content.xpath("./td[2]/a/text()")[0].strip()
        if name == "":
            name = content.xpath("./td[2]/a")[0].xpath("string(.)").strip()
        ggstart_time = content.xpath("./td[3]/text()")[0].strip()
        url = "http://www.fcgggzy.cn" + content.xpath("./td[2]/a/@href")[0]
        temp = [name, ggstart_time, url]
        data.append(temp)
    df = pd.DataFrame(data=data)
    df["info"]=None
    return df


def f2(driver):
    locator = (By.ID,"MoreInfoList1_Pager")
    WebDriverWait(driver,20).until(EC.visibility_of_element_located(locator))
    total_page = driver.find_element_by_xpath("//div[@id='MoreInfoList1_Pager']/table//font[2]").text
    driver.quit()
    return int(total_page)

def f3(driver, url):
    driver.get(url)
    locator = (By.ID, "tblInfo")
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
    div = soup.find('table', id='tblInfo')
    return div


data =[

    ["zfcg_zhaobiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_biangeng_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_kongzhijia_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004005/MoreInfo.aspx?CategoryNum=001004005",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_yucai_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004009/MoreInfo.aspx?CategoryNum=001004009",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_zhongbiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["zfcg_liubiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004007/MoreInfo.aspx?CategoryNum=001004007",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_biangeng_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_kongzhijia_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiaohx_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001006/MoreInfo.aspx?CategoryNum=001001006",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_liubiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001008/MoreInfo.aspx?CategoryNum=001001008",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_shuili_zhaobiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011001/MoreInfo.aspx?CategoryNum=001011001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_shuili_biangeng_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011002/MoreInfo.aspx?CategoryNum=001011002",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_shuili_kongzhijia_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011003/MoreInfo.aspx?CategoryNum=001011003",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_shuili_zhongbiaohx_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011008/MoreInfo.aspx?CategoryNum=001011008",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_shuili_zhongbiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011004/MoreInfo.aspx?CategoryNum=001011004",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_shuili_liubiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011006/MoreInfo.aspx?CategoryNum=001011006",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_jiaotong_zhaobiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010001/MoreInfo.aspx?CategoryNum=001010001",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_jiaotong_biangeng_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010002/MoreInfo.aspx?CategoryNum=001010002",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_jiaotong_kongzhijia_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010003/MoreInfo.aspx?CategoryNum=001010003",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_jiaotong_zhongbiaohx_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010008/MoreInfo.aspx?CategoryNum=001010008",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_jiaotong_zhongbiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010004/MoreInfo.aspx?CategoryNum=001010004",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_jiaotong_liubiao_gg",
     "http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010006/MoreInfo.aspx?CategoryNum=001010006",
     ["name", "ggstart_time", "href", "info"], f1, f2],
]

def work(conp,**arg):
    est_meta(conp, data=data, diqu="广西省防城港市",**arg)
    est_html(conp, f=f3,**arg)



if __name__ == "__main__":


    conp=["postgres", "since2015", "192.168.3.171", "guangxi", "fangchenggang"]
    import sys
    arg=sys.argv
    if len(arg) >3:
        work(conp,num=int(arg[1]),total=int(arg[2]),html_total=int(arg[3]))
    elif len(arg) == 2:
        work(conp, html_total=int(arg[1]))
    else:
        work(conp)