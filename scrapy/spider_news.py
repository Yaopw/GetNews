import requests
from lxml import etree
import sys
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.keys import Keys  # 按键
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import datetime
import os
import time
from threading import Timer


# 程序主要运行
def work():
    list_zi = []
    ti = 1
    if not os.path.exists('../scrapy/newsArticle/'):
        os.mkdir('../scrapy/newsArticle/')

    url = 'https://news.baidu.com/'  # 网页首页 标题页面
    headers = {
        'Cookie': 'BIDUPSID=9984B255B4C6CE9D5F13342A2A8C04CB; PSTM=1660564985; BAIDUID=20B0318F2C58882251AA38560E7DE6E4:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=7; BAIDUID_BFESS=20B0318F2C58882251AA38560E7DE6E4:FG=1; BDRCVFR[C0p6oIjvx-c]=I67x6TjHwwYf0; BCLID=10843889608616252747; BCLID_BFESS=10843889608616252747; BDSFRCVID=2mAOJeC627t9RFOjjCgceZfm70O4gmQTH6ao-oKZTGjFsRi29LiuEG0PLU8g0KuM5gtGogKKX2OTHNLF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; BDSFRCVID_BFESS=2mAOJeC627t9RFOjjCgceZfm70O4gmQTH6ao-oKZTGjFsRi29LiuEG0PLU8g0KuM5gtGogKKX2OTHNLF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=Jn4toIKbJK_3ejrlKDTjhPrMDxcCWMT-0bFH_--XLqQcjRcJbPbqW4KDjN39tPbLLGn7_JjOHR7voxbjMxj504cXetv0-xQxtNRr-Cnjtpvh8D5T5MJobUPUWa59LUvwBgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj0DKLK-oj-D_9j63P; H_BDCLCKID_SF_BFESS=Jn4toIKbJK_3ejrlKDTjhPrMDxcCWMT-0bFH_--XLqQcjRcJbPbqW4KDjN39tPbLLGn7_JjOHR7voxbjMxj504cXetv0-xQxtNRr-Cnjtpvh8D5T5MJobUPUWa59LUvwBgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj0DKLK-oj-D_9j63P; H_PS_PSSID=36549_36920_37584_36885_37627_37721_37539_37714_26350; BA_HECTOR=ah802104a405858g8ha42vma1hmc1ud1f; ZFY=nevjGiGUTp7lUNogX59jNd3DbLwYt2c3ZvtRyGFbcck:C; LOCALGX=%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30; Hm_lvt_e9e114d958ea263de46e080563e254c4=1667631060; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1667631060',
        'Referer': 'https://www.baidu.com/link?url=jTzCrAc24iH28UJHZjOUEdxkv0cT6Vth4c0Vs8wplWu3iU1vVtClWwFrFWH89SpN&wd=&eqid=970d09aa0002711500000006636607cd',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    r = requests.get(url=url, headers=headers)
    data_text = r.text
    with open('data_text.html', 'wb') as f:
        f.write(r.content)
    xml = etree.HTML(data_text)
    data = xml.xpath('//div[@id="pane-news"]/div[@class="hotnews"]/ul/li/strong//text()')  # 获取标题
    list_text = []  # 创建获取标题列表
    list_link = []  # 创建获取标题链接
    for i in data:
        if i == '\n':
            continue
        elif i == '\xa0':
            continue
        else:
            list_text.append(i)  # 获取的标题保存到列表里
    data2 = xml.xpath('//div[@id="pane-news"]/ul[@class="ulist focuslistnews"]/li//a/text()')  # 获取标题
    list_text = list_text + data2  # 最终获取到的标题列表

    data3 = xml.xpath('//div[@id="pane-news"]/div[@class="hotnews"]/ul/li/strong/a/@href')  # 获取链接
    list_link = data3
    data4 = xml.xpath('//div[@id="pane-news"]/ul[@class="ulist focuslistnews"]/li//a/@href')  # 获取链接
    list_link = list_link + data4  # 获取最终文章链接
    print('===' * 20)
    print(list_text)
    print(list_link)
    print(len(list_text))
    print(len(list_link))

    s=Service(r'chromedriver.exe')
    options=webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # driver = webdriver.Chrome(executable_path='G:\临时\百度新闻_t-9095\chromedriver.exe')  # 启动浏览器
    driver=webdriver.Chrome(service=s,options=options)
    vido_if = None
    for i, url2 in enumerate(list_link):
        list_end = []  # 创建空列表 方便获取最后的内容
        print('==='*20)
        print(list_link[i])  # 打印文章链接
        print(list_text[i])  # 打印文章标题
        list_end.append('文章链接：' + list_link[i])  #######################
        list_end.append('文章标题：' + list_text[i])  #######################
        time.sleep(1)
        vio_past = None
        try:
            driver.get(url2)  # 浏览器获取文章链接
        except TimeoutException as te:
            # 保存获取的内容到txt文件，以时间命名
            t = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
            list_zi = list_zi + list_end
            with open('../scrapy/newsArticle/' + t + '.txt', 'w', encoding='utf-8') as f:
                for m in list_end:
                    f.write(m + '\n')
            print('---get问题**************************************************************************')
            print(te)
            print(url2)
            vido_if = None
            continue
        wait = WebDriverWait(driver, 10)
        wait1 = WebDriverWait(driver, 1)
        # 清洗网页格式
        wait.until(EC.presence_of_element_located((By.XPATH, '//p')))
        try:
            time.sleep(4)
            driver.set_page_load_timeout(4)
            wait1.until(EC.presence_of_element_located((By.XPATH, '//div[@class="pagebase-left-switch"]')))
            wait1.until(EC.presence_of_element_located((By.XPATH, '//a[@id="TANGRAM__PSP_4__closeBtn"]')))
            vido_if = driver.find_elements(By.XPATH, '//div[@class="pagebase-left-switch"]')
            vido_close = driver.find_element(By.XPATH, '//a[@id="TANGRAM__PSP_4__closeBtn"]')
            vido_close.click()
            vido_if = True
            vio_past = 1
        except NoSuchElementException:
            vido_if = None
        except TimeoutException:
            vido_if = None

        if vido_if:
            vido_if = None
            # 保存获取的内容到txt文件，以时间命名
            t = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
            list_zi = list_zi + list_end
            with open('../scrapy/newsArticle/'+ t + '.txt', 'w', encoding='utf-8') as f:
                for k in list_end:
                    f.write(k + '\n')
            continue
        elif not vido_if:
            try:
                click1 = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div[3]/div[1]/div/i')  # 确保内容获取完整
                click1.click()
            except NoSuchElementException:
                print('')
            content = driver.find_elements(By.XPATH, '//div[@class="left_zw"]//p')
            if not content:
                content = driver.find_elements(By.XPATH, '//div[@class="u-mainText"]//p')
            if not content:
                content = driver.find_elements(By.XPATH, '//article[@class="article-content  "]')
            if not content:
                if not vido_if:
                    content = driver.find_elements(By.XPATH, '//p')
            try:
                driver.find_element(By.XPATH, '//div[@class="close-btn"]').click()
                click2 = driver.find_element(By.XPATH, '//span[@class="m-icon"]')  # 确保内容获取完整
                print(click2)
                click2.click()
                content = driver.find_elements(By.XPATH, '//section[@class="main-text-container"]')
            except NoSuchElementException:
                print('')
            arg = 1
            if content:
                for contents in content:
                    if arg:
                        vido_if = None
                        if '央视新闻客户端' in contents.text:
                            break
                        elif '万粉丝 ·' in contents.text:
                            list_end.remove(list_end[-1])
                            break
                        elif '责任编辑：' in contents.text:
                            print(contents.text)
                            list_end.append(contents.text)  #######################
                            arg = 0
                        elif '责编：' in contents.text:
                            print(contents.text)
                            list_end.append(contents.text)  #########list_end##############
                            arg = 0
                        else:
                            print(contents.text)
                            list_end.append(contents.text)  #######################


        # 保存获取的内容到txt文件，以时间命名
        t = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        list_zi = list_zi + list_end
        with open('../scrapy/newsArticle/' + t + '.txt', 'w', encoding='utf-8') as f:
            for m in list_end:
                f.write(m + '\n')
        vido_if = None
    print('爬取完毕')
    return ti, list_zi


if __name__ == '__main__':
    ti, list_zi = work()