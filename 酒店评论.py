from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import os
from lxml import etree
import threading
import base64
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import csv



option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=option)





# 爬取一个站点的评论信息
class ScrapyOne(object):

    def __init__(self, url):
        super(ScrapyOne, self).__init__()
        # 站点url
        self.url = url
        # 当前爬取的页
        self.page = 1
        # 评价总页数
        self.allPage = 1
        # 使用Chrome浏览器
        self.driver = Chrome(options=option)
        # 重新点击次数
        self.retryNum = 5

    # 翻页
    def nextPage(self):
        try:
            self.page += 1
            # 一下的代码可能由于页面的刷新报错，因此这里使用了try-catch
            # 清空页码输入框
            self.driver.find_elements_by_id("cPageNum")[0].clear()
            # 输入下一页的页码
            self.driver.find_elements_by_id("cPageNum")[0].send_keys(self.page)
            # 点击翻页按钮
            self.driver.find_elements_by_id('cPageBtn')[0].click()
            # 获取当前的页码
            currentPage = int(self.driver.find_elements_by_xpath("//*/a[@class='current']/span")[
                0].text)
            while currentPage != self.page:
                # 这里的休眠十分重要，最好设置大一点，不然可能什么也爬不到
                time.sleep(3)
                self.driver.find_elements_by_id("cPageNum")[0].clear()
                self.driver.find_elements_by_id(
                    "cPageNum")[0].send_keys(self.page)
                self.driver.find_elements_by_id('cPageBtn')[0].click()
                currentPage = int(self.driver.find_elements_by_xpath("//*/a[@class='current']/span")[
                    0].text)
            self.retryNum = 5#不知道啥意思
        except Exception as e:
            # 重试次数超过5次，结束翻页
            if self.retryNum == 0:
                return False
            # 如果不是爬到最后一页
            if self.page <= self.allPage:
                # 页码回滚
                self.page -= 1
                # 刷新当前页面
                self.driver.refresh()
                time.sleep(3)
                self.retryNum -= 1
                # 继续翻页
                self.nextPage()

    # 爬取评论信息
    def scrapyComment(self):
        data = etree.HTML(self.driver.page_source)
        path="//div[@class='comment_block J_asyncCmt']"
        path1="//span[@class='small_c']/@data-value"
        path2="//span[@class='score']/span/text()"
        path3="//span[@class='type']/text()"
        path4="//span[@class='date']/text()"
        path5="//a[@class='room J_baseroom_link room_link']/text()"
        path6="//a[@class='useful']/@data-voted"
        path7="//div[@class='J_commentDetail']/text()"
        # 使用Xpath获取评价
        for i in range(1,16):
            if data.xpath(path+str([i])):
                path1_=path+str([i])+path1
                path2_=path+str([i])+path2
                path3_=path+str([i])+path3
                path4_=path+str([i])+path4
                path5_=path+str([i])+path5
                path6_=path+str([i])+path6
                path7_=path+str([i])+path7
                scores=str(data.xpath(path1_)).strip("'[]'")
                sum_score=str(data.xpath(path2_)).strip("''[]")
                types=str(data.xpath(path3_)).strip("''[]")
                date=str(data.xpath(path4_)).strip("'[]'")
                room=str(data.xpath(path5_)).strip("''[]")
                useful=str(data.xpath(path6_)).strip("''[]")
                text=str(data.xpath(path7_)).strip("''[]")
               
                res=[]
                res.extend([scores,sum_score,types,date,room,useful,text])
                self.save(res)


        print('[%s]\t%s\t第%s页爬取完成' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.url, self.page))

    # 获取当前站点的评价信息总共有多少页
    def getPage(self):
        return int(self.driver.find_element_by_xpath(
            "//*[@id='divCtripComment']/div[4]/div/div[1]/a[7]/span").text)

    # 保存评价信息
    def save(self,item):

        filename=str(self.url).split('.')[2].split('/')[2]
        filepath="D:\PythonCodes\Python_Course_Project/"+filename+'.csv'
        with open(filepath,'a',newline='',encoding='utf_8_sig') as f:
            writer = csv.writer(f)
            writer.writerow(item)
            f.close()
    # def save(self, line):    #
    #     with open(file, 'a', encoding='UTF-8-sig') as f:
    #         f.write(line + '\n')

    def main(self):
        # 这里会打开Chrome浏览器
        self.driver.get(self.url)
        self.allPage = self.getPage()
        # 点击查看评价的按钮
        # self.driver.find_element_by_id('commentTab').click()
        while self.page <= self.allPage:
            # 爬取评价
            self.scrapyComment()
            # 翻页
            self.nextPage()
        print('爬取完成', self.url)
        # 关闭当前浏览器窗口
        self.driver.close()


# 爬取线程
class ScrapyThread(threading.Thread):

    def __init__(self, url):
        super(ScrapyThread, self).__init__()
        self.url = url

    def run(self):
        # 爬取一个站点
        one = ScrapyOne(self.url)
        one.main()

if __name__ == "__main__":
    # 站点列表
    urlList = ['https://hotels.ctrip.com/hotel/437904.html#ctm_ref=hod_hp_sb_lst',   # 大连友谊宾馆
              'https://hotels.ctrip.com/hotel/400693.html#ctm_ref=hod_hp_sb_lst',    # 大连香格里拉酒店
              'https://hotels.ctrip.com/hotel/371177.html#ctm_ref=hod_hp_sb_lst']    # 大连富丽华酒店]
    for url in urlList:
        # 创建爬取线程
        thread = ScrapyThread(url)
        thread.start()

