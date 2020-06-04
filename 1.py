from selenium import webdriver
import time
import requests
import re
import bs4
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame

class Graduate:
    def __init__(self,url):
        self.head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKi"
                          "t/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }
        self.data = []


    def get_school_data(self, url):
        """返回第一页所有专业的url"""
        response = requests.get(url, headers=self.head)
        response.raise_for_status()
        html = response.text
        school_url = re.findall('<td class="ch-table-center"><a href="(.*?)" '
                                    'target="_blank">查看</a>', html)
        return school_url


    def get_school_data2(self, url):
        """返回第二页所有专业的url"""
        driver = webdriver.Chrome()          #创建浏览器对象
        driver.get(url)
        time.sleep(3)  
        driver.find_element_by_xpath("//li[@class='lip lip-last']").click()  
        time.sleep(3)
        page=driver.page_source
        school_url2 = re.findall('<td class="ch-table-center"><a href="(.*?)" '
                                        'target="_blank">查看</a>', page)
        return school_url2


    def get_final_data(self, url):
        """输出一个学校一个学院一个专业的数据"""
        temp = []
        response = requests.get(url, headers=self.head)
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        summary = soup.find_all('td', {"class": "zsml-summary"})
        summary2 = soup.find_all('tbody',{"class": "zsml-res-items"})
        v=summary2[0].get_text()
        for x in summary:
            temp.append(x.get_text())
        temp.append(v)
        self.data.append(temp)

    def get_speciality_data(self):
        """获取所有学校的数据"""
        url = "http://yz.chsi.com.cn"
        speciality_url1 = self.get_school_data(start_url)
        speciality_url2 = self.get_school_data2(start_url)
        amount = len(speciality_url1)+len(speciality_url2)
        i = 0
        for speciality_url1 in speciality_url1:
            i += 1
            url_ = url + speciality_url1
            # 找到一个学校对应所有满足学院网址
            print("已完成第" + str(i) + "/" + str(amount) + "专业爬取")
            time.sleep(1)
            self.get_final_data(url_)
        for speciality_url2 in speciality_url2:
            i += 1
            url_ = url + speciality_url2
            # 找到一个学校对应所有满足学院网址
            print("已完成第" + str(i) + "/" + str(amount) + "专业爬取")
            time.sleep(1)
            self.get_final_data(url_)

    def get_data_frame(self):
        """将列表形数据转化为数据框格式"""
        data = DataFrame(self.data)
        data.to_csv("查询招生信息.csv", encoding="utf_8_sig")

 
if __name__ == '__main__':
    dict1= {
            "北京市":11,"天津市":12,"河北省":13,"山西省":14,"内蒙古自治区":15,"辽宁省":21,
            "吉林省":22,"黑龙江省":23,"上海市":31,"江苏省":32,"浙江省":33,"安徽省":34,"福建省":35,
            "江西省":36,"山东省":37,"河南省":41,"湖北省":42,"湖南省":43,"广东省":44,"广西壮族自治区":45,
            "海南省":46,"重庆市":50,"四川省":51,"贵州省":52,"云南省":53,"西藏自治区":54,"陕西省":61,
            "甘肃省":62,"青海省":63,"宁夏回族自治区":64,"新疆维吾尔自治区":65
            }

    dict2= {
            "哲学":int("01"),"经济学":int("02"),"法学":int("03"),"教育学":int("04"),"文学":int("05"),"历史学":int("06"),"理学":int("07"),
            "工学":int("08"),"农学":int("09"),"医学":10,"军事学":11,"管理学":12,"艺术学":13
            }

    city="上海市"
    university="上海理工大学"
    speciality="管理学"
    start_url = "https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm="+str(dict1[city])+"&dwmc="+university+"&mldm="+str(dict2[speciality])+"&mlmc="+university+"&yjxkdm=&xxfs=&zymc=####"
    spyder = Graduate(start_url)
    spyder.get_speciality_data()
    spyder.get_data_frame()